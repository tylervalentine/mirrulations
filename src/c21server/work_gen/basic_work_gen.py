import random
import time
import redis


def generate_jobs(database, start_key=None):
    if start_key is None:
        start_key = random.randint(0, 10)
    for _ in range(10):
        value = random.randint(0, 10)
        print(f"I am generating work {start_key} with value {value}!")
        database.hset("jobs_waiting", start_key, value)
        start_key += 1


def emulate_job_creation(database):
    for current_key in range(1, 50, 10):
        generate_jobs(database, current_key)
        time.sleep(30)


if __name__ == "__main__":
    redis = redis.Redis()
    emulate_job_creation(redis)
