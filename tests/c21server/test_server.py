from fakeredis import FakeStrictRedis
from c21server.work_server.work_server import WorkServer


def test_workserver():
    assert WorkServer(FakeStrictRedis()) is not None
