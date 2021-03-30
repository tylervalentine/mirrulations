from dashboard_server import Dashboard
from redis import Redis

server = create_server(Redis())
app = server.app
