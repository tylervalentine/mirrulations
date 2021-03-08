import redis
import random
import time


def generateJobs(r):
    for i in range(10):
        id = random.randint(0, 10000)
        value = random.randint(0, 10)
        r.hset("jobs_wating", id, value)
        print(id, value)


def emulateJobCreation(r):
    for i in range(5):
        generateJobs(r)
        time.sleep(30)


r = redis.Redis()

try:
    r.ping()
    print('Successfully connected to redis')

    emulateJobCreation(r)

except redis.exceptions.ConnectionError as r_con_error:
    print('Redis connection error')
