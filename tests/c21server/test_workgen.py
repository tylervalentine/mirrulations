from fakeredis import FakeRedis
from pytest import fixture
import c21server.work_gen.basic_work_gen as work_gen


@fixture(name='mock_redis')
def fixture_mock_redis():
    return FakeRedis()


def test_generate_jobs(mock_redis):
    work_gen.generate_jobs(mock_redis, 6)
    assert mock_redis.hlen("jobs_waiting") == 10
    expected_keys = (i for i in range(6, 16))
    keys = mock_redis.hkeys("jobs_waiting")
    for key in keys:
        assert int(key) in expected_keys


def test_emulate_job_creation(mock_redis):
    work_gen.emulate_job_creation(mock_redis)
    assert mock_redis.hlen("jobs_waiting") == 50
    expected_keys = (i for i in range(1, 51))
    keys = mock_redis.hkeys("jobs_waiting")
    for key in keys:
        assert int(key) in expected_keys
