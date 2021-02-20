from c21client.client import dummy_client

def test_dummy():
	assert dummy_client() == 42
