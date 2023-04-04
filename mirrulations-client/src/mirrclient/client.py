# pylint: disable=too-many-locals
import time
import os
import sys
from json import dumps, loads
from flask import jsonify
import requests
import redis
from dotenv import load_dotenv
from mirrclient.saver import Saver
from mirrclient.exceptions import NoJobsAvailableException
from mirrcore.job_queue_exceptions import JobQueueException
from mirrcore.path_generator import PathGenerator
from mirrcore.job_queue import JobQueue


def is_environment_variables_present():
    """
    A boolean function that returns whether environment variables are
    present for performing jobs.

    Returns
    -------
    Boolean
    """
    return (os.getenv('WORK_SERVER_HOSTNAME') is not None
            and os.getenv('WORK_SERVER_PORT') is not None
            and os.getenv('API_KEY') is not None
            and os.getenv('ID') is not None)


class Client:
    """
    The Client class performs jobs given to it by a workserver
    It receives a job, performs it depending on the job type.
    A job is performed by calling an api endpoint to request
    a json object. The Client sends back the results back
    to the workserver.

    Attributes
    ----------
    api_key : str
        Api key used to authenticate requests made to api
    server_validator : ServerValidator
        This is used to validate requests made between the
        workserver and the Client
    client_id : int
        An id that defaults to -1 but is eventually replaced by a
        value from the workserver.
    """

    def __init__(self, redis_server):
        self.api_key = os.getenv('API_KEY')
        self.client_id = os.getenv('ID')
        self.path_generator = PathGenerator()
        self.saver = Saver()
        self.redis = redis_server
        self.job_queue = JobQueue(redis_server)

        hostname = os.getenv('WORK_SERVER_HOSTNAME')
        port = os.getenv('WORK_SERVER_PORT')
        self.url = f'http://{hostname}:{port}'

    def _check_for_database(self):
        """
        Checks if the database is connected
        if not this raises an exception

        Parameters
        ----------
        workserver : WorkServer
            the work server class

        Raises
        ------
        ConnectionError
            if the database is not connected
        """
        self.redis.ping()

    def get_job(self):
        """
        Get a job from the work server.
        Converts API URL to regulations.gov URL and prints to logs.
        From: https://api.regulations.gov/v4/dockets/type_id
        To: https://www.regulations.gov/docket/type_id

        :raises: NoJobsAvailableException
            If no job is available from the work server
        """

        # response = requests.get(f'{self.url}/get_job',
        #                         params={'client_id': self.client_id},
        #                         timeout=10)
        self._check_for_database()
        print("Attempting to get job")
        try:
            if self.job_queue.get_num_jobs() == 0:
                job = {'error': 'No jobs available'}
            job = self.job_queue.get_job()
            print(type(job))
            print("Job received from job queue")
        except JobQueueException:
            job = {'error': 'No jobs available'}


        self.redis.hset('jobs_in_progress', job['job_id'], job['url'])
        self.redis.hset('client_jobs', job['job_id'], self.client_id)

        self.job_queue.decrement_count(job.get('job_type', 'other'))
        print(f'Job received: {job.get("job_type", "other")} for client: ', self.client_id)

        link = 'https://www.regulations.gov/'
        if 'error' in job:
            raise NoJobsAvailableException()
        job = {'job_id': job['job_id'],
                'url': job['url'],
                'job_type': job.get('job_type', 'other'),
                'reg_id': job.get('reg_id', 'other_reg_id'),
                'agency': job.get('agency', 'other_agency')}
        split_url = str(job['url']).split('/')
        job_type = split_url[-2][:-1]  # Removes plural from job type
        type_id = split_url[-1]
        print(f'Regulations.gov link: {link}{job_type}/{type_id}')
        print(f'API URL: {job["url"]}')
        return job

    def send_job(self, job, job_result):
        """
        Returns the job results to the workserver
        If there are any errors in the job_result, the data json is returned
        as  {'job_id': job_id, 'results': job_result}
        else {
            'job_id': job_id, 'results': job_result,
            'directory': output_path
            }

        Parameters
        ----------
        job_id : str
            id for current job
        job_result : dict
            results from a performed job
        """
        data = {
            'job_type': job['job_type'],
            'job_id': job['job_id'],
            'results': job_result,
            # Updated to get reg_id and agency from regulations json
            # - Jack W. 3/14
            'reg_id': job['reg_id'],
            'agency': job['agency']
        }
        print(f'Sending Job {job["job_id"]} to Work Server')
        if 'error' not in job_result:
            data['directory'] = self.path_generator.get_path(job_result)

        self._put_results(data)
        #self.put_results_to_mongo(data)
        comment_has_attachment = self.does_comment_have_attachment(job_result)

        if data["job_type"] == "comments" and comment_has_attachment:
            self.download_all_attachments_from_comment(data, job_result)

    def _put_results(self, data):
        """
        Ensures data format matches expected format
        If results are valid, writes them to disk

        Parameters
        ----------
        data : dict
            the results from a performed job
        """
        if any(x in data['results'] for x in ['error', 'errors']):
            print(f"{data['job_id']}: Errors found in results")
            return
        dir_, filename = data['directory'].rsplit('/', 1)
        self.saver.make_path(dir_)
        self.saver.save_json(f'/data{dir_}/{filename}', data)
        print(f"{data['job_id']}: Results written to disk")

    def perform_job(self, job_url):
        """
        Performs job via get_request function by giving it the job_url combined
        with the Client api_key for validation.

        Parameters
        ----------
        job_url : str
            url from a job

        Returns
        -------
        dict
            json results of the performed job
        """
        print('Performing job')
        try:
            if "?" in job_url:
                return requests.get(job_url + f'&api_key={self.api_key}',
                                    timeout=10).json()
            return requests.get(job_url + f'?api_key={self.api_key}',
                                timeout=10).json()
        except requests.exceptions.ReadTimeout:
            return {"error": "Read Timeout"}

    def download_all_attachments_from_comment(self, data, comment_json):
        '''
        Downloads all attachments for a comment

        Parameters
        ----------
        data : dict
            Dictionary of the job
            Keys include: 'job_type', 'job_id', 'results', 'reg_id', 'agency'

        comment_json : dict
            The json of the comment

        '''

        path_list = self.path_generator.get_attachment_json_paths(comment_json)
        counter = 0
        comment_id_str = f"Comment - {comment_json['data']['id']}"
        print(f"Found {len(path_list)} attachment(s) for {comment_id_str}")
        for included in comment_json["included"]:
            attributes = included["attributes"]
            if (attributes["fileFormats"] and
                    attributes["fileFormats"] not in ["null", None]):
                for attachment in included['attributes']['fileFormats']:
                    url = attachment['fileUrl']
                    self.download_single_attachment(url, path_list[counter],
                                                    data)
                    print(f"Downloaded {counter+1}/{len(path_list)} "
                          f"attachment(s) for {comment_id_str}")
                    counter += 1

    def download_single_attachment(self, url, path, data):
        '''
        Downloads a single attachment for a comment and
        writes it to its correct path
        Also puts the attachment 'data' dict to the work server for mongo entry

        Parameters
        ----------
        url : str
            The attachment download url
            Ex: http://downloads.regulations.gov/####

        path : str
            The attachment path the download should be written to
            Comes from the path_generator.get_attachment_json_paths

        data : dict
            Dictionary of the job
            Keys include: 'job_type', 'job_id', 'results', 'reg_id', 'agency'

        '''
        response = requests.get(url, timeout=10)
        dir_, filename = path.rsplit('/', 1)
        self.saver.make_path(dir_)
        self.saver.save_attachment(f'/data{dir_}/{filename}', response.content)
        print(f"SAVED attachment - {url} to path: ", path)
        filename = path.split('/')[-1]
        data = self.add_attachment_information_to_data(data, path, filename)
        #self.put_results_to_mongo(data)

    def add_attachment_information_to_data(self, data, path, filename):
        data['job_type'] = 'attachments'
        data['attachment_path'] = f'/data/data{path}'
        data['attachment_filename'] = filename
        return data

    def put_results_to_mongo(self, data):
        requests.put(f'{self.url}/put_results', json=dumps(data),
                     params={'client_id': self.client_id},
                     timeout=10)

    def does_comment_have_attachment(self, comment_json):
        """
        Validates whether a json for a comment has any
        attachments to be downloaded.

        RETURNS
        -------
        True or False depending if there is an attachment
        available to download from a comment
        """
        if "included" in comment_json and len(comment_json["included"]) > 0:
            return True
        return False

    def job_operation(self):
        """
        Processes a job.
        The Client gets the job from the workserver, performs the job
        based on job_type, then sends back the job results to
        the workserver.
        """
        print('Processing job from work server')
        job = self.get_job()
        result = self.perform_job(job['url'])
        self.send_job(job, result)
        if any(x in result for x in ('error', 'errors')):
            print(f'FAILURE: Error in {job["url"]}\nError: {result["error"]}')
        else:
            print(f'SUCCESS: {job["url"]} complete')


if __name__ == '__main__':
    load_dotenv()
    if not is_environment_variables_present():
        print('Need client environment variables')
        sys.exit(1)

    try:
        r = redis.Redis('redis')
        r.keys('*')
    except redis.exceptions.ConnectionError:
        print('There is no Redis database to connect to.')
        sys.exit(1)

    client = Client(r)

    while True:
        try:
            client.job_operation()
        except NoJobsAvailableException:
            print("No Jobs Available")
        time.sleep(3.6)
