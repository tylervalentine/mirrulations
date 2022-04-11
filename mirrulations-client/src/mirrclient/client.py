import time
import os
import sys
import base64
from json import dumps, loads
import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError as RequestConnectionError
from requests.exceptions import HTTPError


class NoJobsAvailableException(Exception):
    """
    Raises an Exception when there are no jobs available in the workserver.
    """

    def __init__(self, message="There are no jobs available"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


def perform_attachment_job(url, api_key, job_id):
    """
    Performs an attachment job via get_request function by giving
    it the job_url combined with the Client api_key for validation.

    Parameters
    ----------
    job_url : str
        url from a job

    Returns
    -------
    json results of the performed attachment job
    """
    attachments = {} # attachment_name : encoded_file
    url = url + f'?api_key={api_key}'
    response_from_related = requests.get(url)

    response_from_related = response_from_related.json()

    file_info = response_from_related["data"][0]["attributes"]["fileFormats"]
    file_urls = []
    file_types = []
    for link in file_info:
        file_urls.append(link["fileUrl"])
        file_types.append(link["format"])

    for i, (link, file_type) in enumerate(zip(file_urls, file_types)):
        attachment = requests.get(link)
        attachments[f'{job_id}_{i}.{file_type}'] = base64.b64encode(attachment.content).decode('ascii')

    return attachments


def get_key_path_string(results, key):
    """
    Creates path for keys in results

    Parameters
    ----------
    results : dict
        The results of a performed job

    key : str
        A key in the result
    """
    if key in results.keys():
        if results[key] is None:
            return 'None/'
        return results[key] + "/"
    return ""


def get_output_path(results):
    """
    Takes results from a performed job and creates an output
    path for a directory.

    Parameters
    ----------
    results : dict
        the results from a performed job

    Returns
    -------
    str
        the output path for the job
    """
    if 'error' in results:
        return -1
    output_path = ""
    data = results["data"]["attributes"]
    # print(data + "printing data")
    output_path += get_key_path_string(data, "agencyId")
    output_path += get_key_path_string(data, "docketId")
    output_path += get_key_path_string(data, "commentOnDocumentId")
    output_path += results["data"]["id"] + "/"
    output_path += results["data"]["id"] + ".json"
    return output_path


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
            and os.getenv('API_KEY') is not None)


def get_request(url, **kwargs):
    """
    Requests and handles exceptions for GET request.

    Parameters
    ----------
    url : str
        the url for the request
    """
    try:
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        return response
    except (HTTPError, RequestConnectionError):
        print('There was an error handling this response.')
        return response
        # time.sleep(sleep_time)


def put_request(url, data, params):
    """
    Requests and handles exceptions for PUT request.

    Parameters
    ----------
    url : str
        the url for the request
    data : dict
        data sent to the endpoint
    params : dict
        additional arguments sent to the endpoint
    """
    try:
        requests.put(url, json=dumps(data), params=params)

    except (HTTPError, RequestConnectionError):
        print('There was an error handling this response.')


class ServerValidator:
    """
    Validates requests made for the workserver.
    It's main purpose is to deal with HTTP requests and handle request
    exceptions.

    Attributes
    ----------
    server_url : str
        The url for the workserver
    """

    def __init__(self, server_url):
        self.server_url = server_url

    def get_request(self, endpoint, **kwargs):
        """
        Appends the given endpoint to the server url and makes a get request.

        Returns
        -------
        Response
            Json response from request
        """
        return get_request(
            f'{self.server_url}' + endpoint, **kwargs)

    def put_request(self, endpoint, data, params):
        return put_request(
            f'{self.server_url}' + endpoint, data, params)


class Client:
    """
    The Client class performs jobs given to it by a workserver
    It recieves a job, performs it depending on the job type.
    A job is performed by calling an api endpoint to request
    a json obect. The Client sends back the results back
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

    def __init__(self, server_validator):
        self.api_key = os.getenv('API_KEY')
        self.server_validator = server_validator
        self.client_id = -1

    def get_id(self):
        """
        Retrieves an id for the Client from the workserver.
        That value is saved to client_id then written to
        a client.cfg file.
        """
        response = self.server_validator.get_request('/get_client_id')
        self.client_id = int(response.json()['client_id'])
        with open('client.cfg', 'w', encoding='utf8') as file:
            file.write(str(self.client_id))

    def get_job(self):
        """
       The client will use its server validator to request a job
       from its workserver.
       This receives a json in this format:
           {'job': {id: url, 'job_type': job_type}}
       then pulls the job_id, url and job_type from the json.

       Raises
       ------
       NoJobsAvailableException()
           If no job is available from the work server
           requested by the validator.

       Returns
       -------
        tuple
            a tuple containing job_id, url, and job_type
       """
        print('performing job')
        response = self.server_validator.get_request(
            '/get_job', params={'client_id': self.client_id})
        job = loads(response.text)
        if 'error' in job:
            raise NoJobsAvailableException()

        job = job['job']
        job_id = list(job.keys())[0]
        url = job[job_id]
        job_type = job['job_type']
        return job_id, url, job_type

    def send_job(self, job_id, job_result):
        """
        Returns the job results to the workserver via the server_validator.
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
            'job_id': job_id,
            'results': job_result
        }
        if 'errors' not in job_result:
            data['directory'] = get_output_path(job_result)
        self.server_validator.put_request(
            '/put_results', data, {'client_id': self.client_id})

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
        return get_request(
            job_url + f'?api_key={self.api_key}').json()

    def job_operation(self):
        """
        Processes a job.
        The Client gets the job from the workserver, performs the job
        based on job_type, then sends back the job results to
        the workserver.
        """
        job_id, job_url, job_type = self.get_job()
        if job_type == 'attachments':
            result = perform_attachment_job(job_url, job_id)
        else:
            result = self.perform_job(job_url)
        self.send_job(job_id, result)


if __name__ == '__main__':
    load_dotenv()
    if not is_environment_variables_present():
        print('Need client environment variables')
        sys.exit(1)
    work_server_hostname = os.getenv('WORK_SERVER_HOSTNAME')
    work_server_port = os.getenv('WORK_SERVER_PORT')

    validator_for_server = ServerValidator(
        f'http://{work_server_hostname}:{work_server_port}')
    client = Client(validator_for_server)
    client.get_id()

    print('Your ID is: ', client.id)
    while True:
        try:
            client.job_operation()
        except NoJobsAvailableException:
            print("No Jobs Available")
        time.sleep(3.6)
