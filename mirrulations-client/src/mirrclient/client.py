import re
import time
import os
import sys
from json import dumps, loads, load
from dotenv import load_dotenv
from mirrserver.work_server import get_job
import requests
from requests.exceptions import ConnectionError as RequestConnectionError
from requests.exceptions import HTTPError, RequestException


class NoJobsAvailableException(Exception):
    def __init__(self, message="There are no jobs available"):
            self.message = message
            super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'

class Client:

    def __init__(self):
        work_server_hostname = os.getenv('WORK_SERVER_HOSTNAME')
        work_server_port = os.getenv('WORK_SERVER_PORT')
        self.url = f'http://{work_server_hostname}:{work_server_port}'
        self.api_key = os.getenv('API_KEY')
        self.client_id = -1

    def get_client_id(self):
        client_id = read_client_id('client.cfg')
        if client_id == -1:
            client_id = self.request_client_id()
        self.client_id = client_id

    def request_client_id(self):
        endpoint = f'{self.url}/get_client_id'
        response = assure_request(requests.get, endpoint)
        client_id = int(response.json()['client_id'])
        self.write_client_id('client.cfg')
        return client_id

    def get_job(self):
        endpoint = f'{self.url}/get_job'
        params = {'client_id': self.client_id}
        # response = requests.get(endpoint, params=params)
        # response_text = loads(response.text)

        response_text = loads((requests.get(endpoint, params=params)).text)
        if 'job' not in response_text:
            raise NoJobsAvailableException()
        job = response_text['job']
        job_id = list(job.keys())[0]
        url = job[job_id]
        if 'job_type' in job:
            job_type = job['job_type']
        else:
            job_type = 'other'
        return job_id, url, job_type

    def send_job_results(self, job_id, job_result):
        endpoint = f'{self.url}/put_results'
        if 'errors' in job_result:
            data = {
                    'job_id': job_id,
                    'results': job_result
                    }
        else:
            data = {'directory': get_output_path(job_result),
                    'job_id': job_id,
                    'results': job_result}
        params = {'client_id': self.client_id}
        # print('****\n\n\n')
        # print(dumps(data))
        # print('****\n\n\n', flush=True)
        requests.put(endpoint, json=dumps(data), params=params)

    def execute_task(self):
        print('Requesting new job from server...')
        job_id, url, job_type = self.get_job()
        print('Received job!')
        print('Sending result back to server...')
        if job_type == 'attachments':
            print("this is an attachment")
            result = perform_attachment_job(url)
            print("this is the result", result)
        else:
            result = self.perform_job(url)
        self.send_job_results(job_id, result)
        print('Job complete!\n')

    def perform_job(self, url):
        print(f'Getting docket at {url}')
        url = url + f'?api_key={self.api_key}'
        json = assure_request(requests.get, url).json()
        print('Done with current job!')
        return json

    def write_client_id(self, filename):
        with open(filename, 'w', encoding='utf8') as file:
            file.write(str(self.client_id))


def perform_attachment_job(url):
    return {"data": {"attachments_text": [str(url)],
                     "type": "attachment",
                     "id": str(url),
                     "attributes": {'agencyId': None,
                                    'docketId': None,
                                    'commentOnDocumentId': None}
                     }}


def read_client_id(filename):
    try:
        with open(filename, 'r', encoding='utf8') as file:
            return int(file.readline())
    except FileNotFoundError:
        return -1


def assure_request(request, url, sleep_time=60, **kwargs):
    while True:
        response = request(url, **kwargs)
        try:
            check_status_code(response)
            response.raise_for_status()
        except RequestConnectionError:
            print('Unable to connect to the server. '
                  'Trying again in a minute...')
            time.sleep(sleep_time)
        except HTTPError:
            print('An HTTP Error occured.')
        except RequestException:
            print('A Request Error occured.')
        if response is not None:
            return response


def check_status_code(response):
    status_code = response.status_code
    if status_code == 403:
        print(response.json()['error'])
    elif status_code > 400:
        print('Server error. Trying again in a minute...')


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
class Validator:
    """
    This class will serve as the middle man between the client and any server or other endpoint.
    This is to soley handle responses and handle exceptions thrown when making http requests.
    """

    def __init__(self):
        pass
    
    def get_request(self, url, sleep_time=60, **kwargs):
        try:
            response = requests.get(url, **kwargs)
            response.raise_for_status()
            return response
        except (HTTPError, RequestConnectionError):
            print('There was an error handling this response.')
            return response
            # time.sleep(sleep_time)
            
    def put_request(self, url, data, params):
        try:
            requests.put(url, json=dumps(data), params=params)

        except (HTTPError, RequestConnectionError):
            print('There was an error handling this response.')


class ServerValidator(Validator):
    def __init__(self, server_url):
        self.server_url = server_url
        super.__init__

    def get_request(self, endpoint, sleep_time=60, **kwargs):
        return super().get_request(f'{self.server_url}' + endpoint, sleep_time, **kwargs)
    
    def put_request(self, endpoint, data, params):
        return super().put_request(f'{self.server_url}' + endpoint, data, params)


class TempClient:
    """
    This will eventually replace the client class. This is created so that Client code can be copied into it
    without removivng any existing code.
    """
    def __init__(self, server_validator, api_validator):
        self.api_key = os.getenv('API_KEY')
        self.server_validator = server_validator
        self.api_validator = api_validator
        self.id = -1
    
    def get_id(self):
        response = self.server_validator.get_request('/get_client_id')
        self.id = int(response.json()['client_id'])
        with open('client.cfg', 'w', encoding='utf8') as file:
            file.write(str(self.id))
        

    def get_job(self):
        response = self.server_validator.get_request('/get_job')
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

        self.server_validator.put_request('/put_results', data, {'client_id': self.id})

    def perform_job(self, job_url):
        return self.api_validator.get_request(job_url + f'?api_key={self.api_key}').json()

    def job_operation(self):
        job_id, job_url, job_type = self.get_job()
        if job_type == 'attachments':
            result = perform_attachment_job(job_url)
        else:
            result = self.perform_job(job_url)
        self.send_job(job_id, result)



if __name__ == '__main__':
    # https://api.regulations.gov/v4/attachments/0900006480cb703d
    load_dotenv()
    if not is_environment_variables_present():
        print('Need client environment variables')
        sys.exit(1)
    client = Client()
    client.get_client_id()
    print('Your ID is: ', client.client_id)
    while True:
        try:
            client.execute_task()
        except NoJobsAvailableException:
            print("No Jobs Available")
        time.sleep(3.6)
