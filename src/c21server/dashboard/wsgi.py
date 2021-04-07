from redis import Redis
from .dashboard_server import create_server

server = create_server(Redis())
app = server.app
