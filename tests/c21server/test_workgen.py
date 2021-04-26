from fakeredis import FakeRedis
from json import load
import requests_mock
from pytest import fixture
import c21server.work_gen.basic_work_gen as work_gen


BASE_URL = 'https://api.regulations.gov/v4/'


@fixture(name='mock_redis')
def fixture_mock_redis():
    return FakeRedis()


@fixture(name='mock_requests')
def fixture_mock_requests():
    return requests_mock.Mocker()


def load_example_data():
    with open('tests/data/dockets_request_example.json') as f:
        return json.load(f)


def test_get_jobs_for_dockets(mock_redis, mock_requests):
    with mock_requests:
        params = {
            'sort': 'lastModifiedDate',
            'page[size]': 250
        }
        mock_requests.get(f'{BASE_URL}/dockets', query_params=params)
        work_gen.get_jobs('dockets', mock_redis)
        expected = 5
        assert len(list(mock_redis.hkeys('jobs_waiting'))) == expected
