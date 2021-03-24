import time
from json import dumps, loads
import requests
from requests.exceptions import ConnectionError as RequestConnectionError
from requests.exceptions import HTTPError, RequestException


class Client:

    def __init__(self):
        self.url = 'http://localhost:8080'
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
        write_client_id('client.cfg', client_id)
        return client_id

    def get_job(self):
        endpoint = f'{self.url}/get_job'
        client_id = self.client_id
        data = {'client_id': client_id}
        job_id, value = request_job(endpoint, data)
        return job_id, value

    def send_job_results(self, job_id, job_result):
        endpoint = f'{self.url}/put_results'
        client_id = self.client_id
        data = {'results': {job_id: int(job_result)}, 'client_id': client_id}
        assure_request(requests.put, endpoint, data=dumps(data))


def execute_client_task(_client):
    print('Requesting new job from server...')
    job_id, value = _client.get_job()
    print('Received job!')
    perform_job(value)
    print('Sending result back to server...')
    _client.send_job_results(job_id, value)
    print('Job complete!\n')


def perform_job(value):
    print(f'I am working for {value} seconds...')
    time.sleep(int(value))
    print('Done with current job!')


def request_job(endpoint, data):
    response = assure_request(requests.get, endpoint,
                              data=dumps(data))
    job = loads(response.text)['job']
    job_id = list(job.keys())[0]
    value = job[job_id]
    return job_id, value


def assure_request(request, url, sleep_time=60, **kwargs):
    while True:
        response = attempt_request(request, url, sleep_time, **kwargs)
        if response is not None:
            return response


def attempt_request(request, url, sleep_time, **kwargs):
    try:
        response = request(url, **kwargs)
        check_status_code(response.status_code)
        response.raise_for_status()
    except RequestConnectionError:
        print('Unable to connect to the server. '
              'Trying again in a minute...')
        time.sleep(sleep_time)
    except (HTTPError, RequestException):
        time.sleep(sleep_time)
    else:
        return response
    return None


def check_status_code(status_code):
    if status_code == 400:
        print('No jobs available. Trying again in a minute...')
    elif status_code > 400:
        print('Server error. Trying again in a minute...')


def read_client_id(filename):
    try:
        with open(filename, 'r') as file:
            return int(file.readline())
    except FileNotFoundError:
        return -1


def write_client_id(filename, client_id):
    with open(filename, 'w') as file:
        file.write(client_id)


if __name__ == '__main__':
    client = Client()
    client.get_client_id()
    print('Your ID is: ', client.client_id)
    while True:
        execute_client_task(client)
