
from mirrcore.redis_check import is_redis_available
from mirrmock.mock_redis import BusyRedis, ReadyRedis


def test_when_redis_loading_is_unavailable():
    database = BusyRedis()
    is_available = is_redis_available(database)
    assert is_available is False


def test_when_redis_done_loading_is_available():
    database = ReadyRedis()
    is_available = is_redis_available(database)
    assert is_available is True
