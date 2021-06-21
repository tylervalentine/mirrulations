from redis import Redis
from mirrserver.work_server import create_server

server = create_server(Redis('redis'))
app = server.app
