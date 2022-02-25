import docker
from redis import Redis
from mirrdash.dashboard_server import create_server

server = create_server(Redis('redis'), docker.from_env(),connect_mongo_db(os.getenv('MONGO_HOSTNAME'),27017))
app = server.app
