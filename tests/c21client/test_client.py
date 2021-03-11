import os
import pytest
import requests
from c21client.client import Client

BASE_URL = "http://localhost:8080"


@pytest.fixture
def setup():
    os.remove('client.cfg')


def test_client_url():
    client = Client()
    assert client.url == BASE_URL


def test_client_gets_existing_client_id():
    client = Client()
    mock_client_id = 99
    path = 'client.cfg'
    with open(path, "w") as file:
        file.write(str(mock_client_id))
    assert mock_client_id == client.get_client_id()


def test_client_gets_client_id_from_server(requests_mock):
    client = Client()
    os.remove('client.cfg')
    mock_client_id = 9
    requests_mock.get(
        '{}/get_client_id'.format(BASE_URL),
        json={'client_id': mock_client_id}
    )
    assert mock_client_id == client.get_client_id()


def test_client_handles_error_when_getting_id_from_server(requests_mock):
    client = Client()
    os.remove('client.cfg')
    requests_mock.get(
        '{}/get_client_id'.format(BASE_URL),
        json={'error': 'Some error'},
        status_code=400
    )
    assert -1 == client.get_client_id()


def test_client_gets_job(requests_mock):
    client = Client()
    requests_mock.get('{}/get_job'.format(BASE_URL), json={1: "1"})
    assert ("1", "1") == client.get_job()


def test_client_handles_error_getting_jobs(requests_mock):
    client = Client()
    requests_mock.get(
        '{}/get_job'.format(BASE_URL),
        json={"Error": "Error message"},
        status_code=400
    )
    try:
        client.get_job()
    except requests.exceptions.HTTPError as exception:
        assert True, 'raised an exception: {}'.format(exception)


# def test_client_sleeps_when_no_jobs_available(requests_mock):
#     client = Client()
#     requests_mock.get(
#         '{}/get_job'.format(BASE_URL),
#         json={"error": "No jobs available"}
#     )
#     client.get_job()


def test_client_sends_job_results(requests_mock):
    client = Client()
    mock_id = 1
    mock_job_result = "1"
    requests_mock.put('{}/put_results'.format(BASE_URL), text='')
    try:
        client.send_job_results(mock_id, mock_job_result)
    except requests.exceptions.HTTPError as exception:
        assert False, 'raised an exception: {}'.format(exception)


def test_client_completes_job_requested(requests_mock):
    client = Client()
    requests_mock.get('{}/get_job'.format(BASE_URL), json={1: "1"})
    requests_mock.put('{}/put_results'.format(BASE_URL), text='')

    try:
        client.complete_client_request()
    except requests.exceptions.HTTPError as exception:
        assert False, 'Raised an exception: {}'.format(exception)
