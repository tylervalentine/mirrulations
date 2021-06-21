from redis import Redis
from dashboard_server import create_server

server = create_server(Redis('redis'))
app = server.app
