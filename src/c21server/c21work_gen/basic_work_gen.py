import redis
import random
import time

r = redis.Redis()


def generateJobs(r):
    for i in range(10):
        id = random.randint(0, 10000)
        value = random.randint(0, 10)
        r.hset("jobs_waiting", id, value)


def emulateJobCreation(r):
    for i in range(5):
        generateJobs(r)
        time.sleep(30)


emulateJobCreation(r)
