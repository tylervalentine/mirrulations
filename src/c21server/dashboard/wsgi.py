from dashboard_server import create_server
from redis import Redis

server = create_server(Redis())
app = server.app
