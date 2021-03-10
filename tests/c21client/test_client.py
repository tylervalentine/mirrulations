import pytest
from c21client.client import Client


BASE_URL = "http://localhost:8080"


def test_client_url():
    client = Client()
    assert client.url == BASE_URL


def test_client_gets_client_id(requests_mock):
    client = Client()
    mock_client_id = 1
    # response subject to change depending on how it will be implemented on the server side
    requests_mock.get('{}/get_client_id'.format(BASE_URL), json={'client_id': 1})
    assert mock_client_id == client.get_client_id()


def test_client_gets_job(requests_mock):
    client = Client()
    requests_mock.get('{}/get_job'.format(BASE_URL), json={1: "1"})
    assert ("1", "1") == client.get_job()


def test_client_sends_job_results(requests_mock):
    client = Client()
    mock_id = 1
    mock_job_result = "1"
    requests_mock.put('{}/put_results'.format(BASE_URL), text='')
    try:
        client.send_job_results(mock_id, mock_job_result)
    except Exception as e:
        assert False, 'raised an exception: {}'.format(e)


def test_client_completes_job_requested(requests_mock):
    client = Client()
    requests_mock.get('{}/get_job'.format(BASE_URL), json={1: "1"})
    requests_mock.put('{}/put_results'.format(BASE_URL), text='')

    try:
        client.complete_client_request()
    except Exception as e:
        assert False, 'Raised an exception: {}'.format(e)

