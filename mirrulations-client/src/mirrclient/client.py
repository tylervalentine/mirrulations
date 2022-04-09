import time
import os
import sys
from json import dumps, loads
import requests
from dotenv import load_dotenv
# from mirrserver.work_server import get_job
from requests.exceptions import ConnectionError as RequestConnectionError
from requests.exceptions import HTTPError


class NoJobsAvailableException(Exception):
    def __init__(self, message="There are no jobs available"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


def perform_attachment_job(url):
    return {"data": {"attachments_text": [str(url)],
                     "type": "attachment",
                     "id": str(url),
                     "attributes": {'agencyId': None,
                                    'docketId': None,
                                    'commentOnDocumentId': None}
                     }}


def get_key_path_string(results, key):
    if key in results.keys():
        if results[key] is None:
            return 'None/'
        return results[key] + "/"
    return ""


def get_output_path(results):
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
    return (os.getenv('WORK_SERVER_HOSTNAME') is not None
            and os.getenv('WORK_SERVER_PORT') is not None
            and os.getenv('API_KEY') is not None)


#######################################
# All code below is part of the refactor.


def get_request(url, **kwargs):
    try:
        response = requests.get(url, **kwargs)
        response.raise_for_status()
        return response
    except (HTTPError, RequestConnectionError):
        print('There was an error handling this response.')
        return response
        # time.sleep(sleep_time)


def put_request(url, data, params):
    try:
        requests.put(url, json=dumps(data), params=params)

    except (HTTPError, RequestConnectionError):
        print('There was an error handling this response.')


class ServerValidator:
    def __init__(self, server_url):
        self.server_url = server_url

    def get_request(self, endpoint, **kwargs):
        return get_request(
            f'{self.server_url}' + endpoint, **kwargs)

    def put_request(self, endpoint, data, params):
        return put_request(
            f'{self.server_url}' + endpoint, data, params)


class Client:

    def __init__(self, server_validator):
        self.api_key = os.getenv('API_KEY')
        self.server_validator = server_validator
        self.client_id = -1

    def get_id(self):
        response = self.server_validator.get_request('/get_client_id')
        self.client_id = int(response.json()['client_id'])
        with open('client.cfg', 'w', encoding='utf8') as file:
            file.write(str(self.client_id))

    def get_job(self):
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
        data = {
                    'job_id': job_id,
                    'results': job_result
                    }
        if 'errors' not in job_result:
            data['directory'] = get_output_path(job_result)
        self.server_validator.put_request(
            '/put_results', data, {'client_id': self.client_id})

    def perform_job(self, job_url):
        return get_request(
            job_url + f'?api_key={self.api_key}').json()

    def job_operation(self):
        job_id, job_url, job_type = self.get_job()
        if job_type == 'attachments':
            result = perform_attachment_job(job_url)
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
