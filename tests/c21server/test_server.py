from c21server.work_server.work_server import WorkServer
from fakeredis import FakeStrictRedis


def test_workserver():
    assert WorkServer(FakeStrictRedis()) is not None
