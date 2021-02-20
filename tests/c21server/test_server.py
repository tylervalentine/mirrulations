from c21server.server import server_dummy

def test_dummy():
	assert server_dummy() == "capstone"
