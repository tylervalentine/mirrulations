from dashboard_server import Dashboard, create_server
from redis import Redis

server = create_server(Redis())
app = server.app
