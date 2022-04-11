import redis
import time
from mirrcore.job_queue import JobQueue
from mirrcore.redis_check import is_redis_available
import json
import pandas as pd
import sys


class AttachmentsGenerator:
    def read_attachments_csv():
        data_frame = pd.read_csv('/home/cs334/capstone2022/attachments_list.csv', usecols=['data.id',
                'data.relationships.attachments.links.related'], dtype={'data.id':'str',
                'data.relationships.attachments.links.related':'str'})
        return data_frame

    def __init__(self, job_queue, database):
        self.job_queue = job_queue
        self.database = database

    def get_job_id(self):
        job_id = self.database.incr('last_job_id')
        return job_id

    def add_job(self, job_type, url):
        job_id = self.get_job_id()
        if job_type == 'attachments':
            job = {'job_id': job_id,
                    'url': url,
                    'job_type': job_type
                }

if __name__ == '__main__':
    database = redis.Redis()
    while not is_redis_available(database):
        print("Redis database is busy loading")
        time.sleep(30)

    job_queue = JobQueue(database)
    generator = AttachmentsGenerator(job_queue, database)


    limit = 5
    attachments_list = []
    counter = 0

    # This is how the attachments generator was working during the last sprint
    data_frame = generator.read_attachments_csv()

    for link in data_frame['data.relationships.attachments.links.related']:
        attachments_list.append(link)

    with open("last_index.txt", "r") as file:
        last_link_index = file.readline()

    with open("last_index.txt", "w") as file:
        for link in attachments_list[int(last_link_index): ]:
           
            if counter > limit:
                sys.exit()

            elif counter < limit:
                job = generator.add_job('data.relationships.attachments.links.related', link)
                counter += 1
                if link == attachments_list[-1]:
                    file.write(str(0))

            elif counter == limit:
                file.write(str(attachments_list.index(link)))
                counter += 1
    

    database.lpush('jobs_waiting_queue', json.dumps(job))
