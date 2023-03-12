import os
import docker
from redis import Redis

from mirrcore.job_queue import JobQueue
from mirrdash.dashboard_server import create_server
from mirrdash.sum_mongo_counts import connect_mongo_db

mongo_host = os.getenv('MONGO_HOSTNAME')
job_queue = JobQueue(Redis('redis'))
server = create_server(job_queue, docker.from_env(),
                       connect_mongo_db(mongo_host, 27017))
app = server.app
