from pytest import fixture
import requests
import requests_mock
from c21client.client import Client, execute_client_task

BASE_URL = 'http://localhost:8080'


@fixture(name='mock_requests')
def fixture_mock_requests():
    return requests_mock.Mocker()


def test_client_url():
    client = Client()
    assert client.url == BASE_URL


def test_client_gets_existing_client_id(mocker):
    client = Client()
    mock_client_id = 99
    write_mock_client_id(mocker)
    read_mock_client_id(mocker, mock_client_id)
    client.get_client_id()
    assert mock_client_id == client.client_id


def test_client_gets_client_id_from_server(mock_requests, mocker):
    client = Client()
    mock_client_id = 9
    read_mock_client_id(mocker, -1)
    write_mock_client_id(mocker)
    with mock_requests:
        mock_requests.get(
            f'{BASE_URL}/get_client_id',
            json={'client_id': mock_client_id}
        )
        client.get_client_id()
        assert mock_client_id == client.client_id


def test_client_gets_job(mock_requests):
    client = Client()
    with mock_requests:
        mock_requests.get(
            f'{BASE_URL}/get_job',
            json={'job': {'1': 1}},
            status_code=200
        )
        assert ('1', 1) == client.get_job()


def test_client_sleeps_when_no_jobs_available(mock_requests, mocker):
    client = Client()
    read_mock_client_id(mocker, 1)
    with mock_requests:
        mock_requests.get(
            f'{BASE_URL}/get_job',
            json={'error': 'No jobs available'},
            status_code=400
        )
        mocker.patch(
            'c21client.client.request_job',
            return_value=('2', 22)
        )
        assert ('2', 22) == client.get_job()


def test_client_sends_job_results(mock_requests, mocker):
    client = Client()
    mock_job_id = 1
    mock_job_result = '1'
    mock_client_id = 999
    read_mock_client_id(mocker, mock_client_id)

    with mock_requests:
        mock_requests.get(
            f'{BASE_URL}/get_client_id',
            json={'client_id': 999},
            status_code=200
        )
        mock_requests.put(
            f'{BASE_URL}/put_results',
            json={'success': 'The job was successfully completed'},
            status_code=200
        )
        try:
            client.send_job_results(mock_job_id, mock_job_result)
        except requests.exceptions.HTTPError as exception:
            assert False, f'raised an exception: {exception}'


def test_client_completes_job_requested(mock_requests, mocker):
    client = Client()
    mock_client_id = 9
    read_mock_client_id(mocker, mock_client_id)

    with mock_requests:
        mock_requests.get(
            f'{BASE_URL}/get_client_id',
            json={'client_id': mock_client_id},
            status_code=200
        )
        mock_requests.get(
            f'{BASE_URL}/get_job',
            json={'job': {'1': 1}},
            status_code=200
        )
        mock_requests.put(
            f'{BASE_URL}/put_results',
            json={'success': 'The job was successfully completed'},
            status_code=200
        )

        try:
            execute_client_task(client)
        except requests.exceptions.HTTPError as exception:
            assert False, f'Raised an exception: {exception}'


def read_mock_client_id(mocker, value):
    mocker.patch(
        'c21client.client.read_client_id',
        return_value=value
    )


def write_mock_client_id(mocker):
    mocker.patch(
        'c21client.client.write_client_id',
        return_value=''
    )
