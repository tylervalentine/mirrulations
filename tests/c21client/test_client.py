from c21client.client import server_url


def test_server_url():
    assert server_url() == "http://localhost:8080"
