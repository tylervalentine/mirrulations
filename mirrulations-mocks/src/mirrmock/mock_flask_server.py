from fakeredis import FakeRedis, FakeServer


def mock_flask_server(create_server):
    redis_server = FakeServer()
    mock_db = FakeRedis(server=redis_server)
    server = create_server(mock_db)
    server.redis_server = redis_server
    server.app.config['TESTING'] = True
    server.client = server.app.test_client()
    return server
