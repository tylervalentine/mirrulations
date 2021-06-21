from redis import Redis
from mirrdash.dashboard_server import create_server

server = create_server(Redis('redis'))
app = server.app
