from c21client.client import Client


def test_client_url():
    client = Client()
    assert client.url == "http://localhost:8080"
