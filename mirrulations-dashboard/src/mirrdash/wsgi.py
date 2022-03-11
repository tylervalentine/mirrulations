import os
import docker
from redis import Redis
from mirrdash.dashboard_server import create_server
from mirrdash.sum_mongo_counts import connect_mongo_db

mongo_host = os.getenv('MONGO_HOSTNAME')
server = create_server(Redis('redis'), docker.from_env(),
                       connect_mongo_db(mongo_host, 27017))
app = server.app
