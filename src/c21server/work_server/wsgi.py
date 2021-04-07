from redis import Redis
from .work_server import create_server

server = create_server(Redis())
app = server.app
