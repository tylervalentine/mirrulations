from functools import partial
from pytest import fixture
import requests
import requests_mock
import c21client.client
from c21client.client import Client, attempt_request
from c21client.client import execute_client_task
from c21client.client import read_client_id, write_client_id


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
    mock_assure_request(mocker)
    mock_get_job(mocker)
    with mock_requests:
        mock_requests.get(
            f'{BASE_URL}/get_job',
            json={'error': 'No jobs available'},
            status_code=400
        )
        assert client.get_job() is None


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


def test_attempt_request_raises_request_exception(mock_requests):
    with mock_requests:
        mock_requests.get(
            f'{BASE_URL}/get_job',
            status_code=400
        )
        response = attempt_request(requests.get, f'{BASE_URL}/get_job', 0)
        assert response is None


def test_attempt_request_raises_connection_exception(mock_requests, mocker):
    mock_raise_connection_error(mocker)
    with mock_requests:
        mock_requests.get(
            f'{BASE_URL}/get_job',
            status_code=400

        )
        response = attempt_request(requests.get, f'{BASE_URL}/get_job', 0)
        assert response is None


def test_check_status_code_greater_than_400(mock_requests):
    with mock_requests:
        mock_requests.get(
            f'{BASE_URL}/get_job',
            status_code=500
        )
        response = attempt_request(requests.get, f'{BASE_URL}/get_job', 0)
        assert response is None


def test_read_client_id_success(tmpdir):
    file = tmpdir.join('test_read.txt')
    file.write('1')
    assert int(file.read()) == read_client_id(str(file))


def test_read_client_id_file_not_found():
    assert read_client_id('nonexistent.txt') == -1


def test_write_client_id(tmpdir):
    file = tmpdir.join('test_write.txt')
    write_client_id(str(file), '1')
    assert file.read() == '1'


def mock_assure_request(mocker):
    mocker.patch(
        'c21client.client.Client.get_job',
        side_effect=partial(c21client.client.attempt_request, sleep_time=0)
    )


def mock_get_job(mocker):
    mocker.patch(
        'c21client.client.Client.get_job',
        return_value=None
    )


def mock_raise_connection_error(mocker):
    mocker.patch(
        'requests.get',
        side_effect=requests.exceptions.ConnectionError
    )


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
