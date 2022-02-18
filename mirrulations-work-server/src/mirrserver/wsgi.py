import time
import redis
from mirrserver.work_server import create_server
from mirrcore.redis_check import is_redis_available

database = redis.Redis('redis')
while not is_redis_available(database):
    print("Redis database is busy loading")
    time.sleep(30)
server = create_server(database)
app = server.app
