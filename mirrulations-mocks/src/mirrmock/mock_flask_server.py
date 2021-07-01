from unittest.mock import MagicMock
from fakeredis import FakeRedis, FakeServer
from mirrmock.mock_data_storage import MockDataStorage


def mock_dashboard_server(create_server):
    redis_server = FakeServer()
    mock_db = FakeRedis(server=redis_server)
    mock_docker = MagicMock()
    server = create_server(mock_db, mock_docker)
    server.redis_server = redis_server
    server.app.config['TESTING'] = True
    server.client = server.app.test_client()
    server.data = MockDataStorage()
    return server


def mock_work_server(create_server):
    redis_server = FakeServer()
    mock_db = FakeRedis(server=redis_server)
    server = create_server(mock_db)
    server.redis_server = redis_server
    server.app.config['TESTING'] = True
    server.client = server.app.test_client()
    server.data = MockDataStorage()
    return server
