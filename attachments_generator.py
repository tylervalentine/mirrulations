import redis
import time
from mirrcore.job_queue import JobQueue
from mirrcore.redis_check import is_redis_available
import random
import json


class AttachmentsGenerator:

    if __name__ == '__main__':
        database = redis.Redis('redis')
        while not is_redis_available(database):
            print("Redis database is busy loading")
            time.sleep(30)
        database.flushdb
        job_queue = JobQueue(database)

        def get_job_id(self):
            job_id = self.database.incr('last_job_id')
            return job_id

        def add_job(self, job_type):
            job_id = self.get_job_id()
            job = {'job_id': job_id,
                    'url': random.randint(0, 6),
                    'job_type': job_type
                }
            return job
        
        for x in range(10):
            if x % 3:
                job = add_job('comments')
                database.lpush('jobs_waiting_queue', json.dumps(job))
                
            if x % 5:
                job = add_job('documents')
                database.lpush('jobs_waiting_queue', json.dumps(job))

            if x % 7:
                job = add_job('dockets')
                database.lpush('jobs_waiting_queue', json.dumps(job))

            else:
                job = add_job('attachments')
                database.lpush('jobs_waiting_queue', json.dumps(job))

