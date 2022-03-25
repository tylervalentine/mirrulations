import redis

class BusyRedis():
    """
    Stub for testing in place of a Redis server that is busy loading the data to memory, 
    ping replies with true
    """
    def ping(self):
        raise redis.BusyLoadingError

class ReadyRedis():
    """
    Stub for testing in place of an active Redis server, 
    ping replies with true
    """
    def ping(self):
        return True


class MockRedisWithStorage():
    """
    Mock for testing in place of an active Redis server that has storage
    """
    def __init__(self, json_like_object):
        self.data = json_like_object


    def set(self, key, value):
        self.data.update({key: value})


    def get(self, key):
        return self.data(f'{key}')