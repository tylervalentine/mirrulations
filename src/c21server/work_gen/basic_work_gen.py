import random
import time
import redis


def generate_jobs(database):
    for _ in range(10):
        key = random.randint(0, 10000)
        value = random.randint(0, 10)
        print(f"I am generating  work with value {value}!")
        database.hset("jobs_waiting", key, value)


def emulate_job_creation():
    database = redis.Redis()
    for _ in range(5):
        generate_jobs(database)
        time.sleep(30)


if __name__ == "__main__":
    emulate_job_creation()
