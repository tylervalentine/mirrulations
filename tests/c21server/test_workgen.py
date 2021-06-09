import json
from fakeredis import FakeRedis
import requests_mock
from pytest import fixture
import c21server.work_gen.work_generator as work_gen


BASE_URL = 'https://api.regulations.gov/v4/dockets'
PARAMS = 'api_key=API_TOKEN&sort=lastModifiedDate&page%5Bsize%5D=250'


@fixture(name='mock_redis')
def fixture_mock_redis():
    return FakeRedis()


@fixture(name='mock_requests')
def fixture_mock_requests():
    return requests_mock.Mocker()


def mock_os_getenv(mocker):
    mocker.patch(
        'c21server.work_gen.work_generator.get_api_key',
        return_value='API_TOKEN'
    )


def load_example_data():
    with open('tests/data/dockets_request_example.json') as file:
        return json.load(file)


def test_get_jobs(mock_redis, mock_requests, mocker):
    with mock_requests:
        url = f'{BASE_URL}?{PARAMS}'
        mock_requests.get(
            url,
            json=load_example_data()
        )
        mock_os_getenv(mocker)
        work_gen.get_jobs('dockets', mock_redis)
        expected = 'dockets/EBSA-2005-0001'
        assert mock_redis.hget('jobs_waiting', 1).decode() == expected
        expected = 'dockets/EBSA-2005-0002'
        assert mock_redis.hget('jobs_waiting', 10).decode() == expected
        assert len(mock_redis.hkeys('jobs_waiting')) == 10
