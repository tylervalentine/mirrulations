from redis import Redis
from work_server import create_server

server = create_server(Redis('redis'))
app = server.app
