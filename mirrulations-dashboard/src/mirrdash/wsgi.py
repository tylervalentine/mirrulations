import docker
from redis import Redis
from mirrdash.dashboard_server import create_server
from mirrdash.sum_mongo_counts import connect_mongo_db
import os

server = create_server(Redis('redis'), docker.from_env(),connect_mongo_db(os.getenv('MONGO_HOSTNAME'),27017))
app = server.app
