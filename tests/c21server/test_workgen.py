from fakeredis import FakeRedis
import pytest
from pytest import fixture
import c21server.work_gen.basic_work_gen as work_gen


@fixture(name='mock_redis')
def fixture_mock_redis():
    return FakeRedis()


def test_generate_jobs(mock_redis):
    work_gen.generate_jobs(mock_redis, 'tests/data/dockets_test_0.txt', 6)
    assert mock_redis.hlen('jobs_waiting') == 10
    # expected_keys = (i for i in range(6, 16))
    expected_values = ["https://api.regulations.gov/v4/dockets/EBSA-2005-0001",
                       "https://api.regulations.gov/v4/dockets/NASA-2005-0001",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0002",
                       "https://api.regulations.gov/v4/dockets/RHS-2005-0001",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0003",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0004",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0005",
                       "https://api.regulations.gov/v4/dockets/NASA-2005-0002",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0006",
                       "https://api.regulations.gov/v4/dockets/EBSA-2005-0002"]

    keys = mock_redis.hkeys('jobs_waiting')
    for key in keys:
        value = mock_redis.hget('jobs_waiting', key).decode("UTF-8")
        assert value in expected_values


def test_generate_jobs_no_start_key(mock_redis):
    work_gen.generate_jobs(mock_redis, 'tests/data/dockets_test_0.txt')
    assert mock_redis.hlen('jobs_waiting') == 10
    # expected_keys = (i for i in range(10))
    expected_values = ["https://api.regulations.gov/v4/dockets/EBSA-2005-0001",
                       "https://api.regulations.gov/v4/dockets/NASA-2005-0001",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0002",
                       "https://api.regulations.gov/v4/dockets/RHS-2005-0001",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0003",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0004",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0005",
                       "https://api.regulations.gov/v4/dockets/NASA-2005-0002",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0006",
                       "https://api.regulations.gov/v4/dockets/EBSA-2005-0002"]

    keys = mock_redis.hkeys('jobs_waiting')
    for key in keys:
        value = mock_redis.hget('jobs_waiting', key).decode("UTF-8")
        assert value in expected_values


def test_generate_jobs_bad_filename(mock_redis):
    with pytest.raises(FileNotFoundError):
        work_gen.generate_jobs(mock_redis, 'tests/data/dockit_test_0.txt')


def test_generate_jobs_bad_data(mock_redis):
    with pytest.raises(Exception):
        work_gen.generate_jobs(mock_redis, 'tests/data/dockets_test_0_bad.txt')

    assert mock_redis.hlen('jobs_waiting') == 3
    # expected_keys = (i for i in range(3))
    expected_values = ["https://api.regulations.gov/v4/dockets/EBSA-2005-0001",
                       "https://api.regulations.gov/v4/dockets/NASA-2005-0001",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0002",
                       "https://api.regulations.gov/v4/dockets/RHS-2005-0001",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0003",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0004",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0005",
                       "https://api.regulations.gov/v4/dockets/NASA-2005-0002",
                       "https://api.regulations.gov/v4/dockets/DOD-2005-0006",
                       "https://api.regulations.gov/v4/dockets/EBSA-2005-0002"]

    keys = mock_redis.hkeys('jobs_waiting')
    for key in keys:
        value = mock_redis.hget('jobs_waiting', key).decode("UTF-8")
        assert value in expected_values
