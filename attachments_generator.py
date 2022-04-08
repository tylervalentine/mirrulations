import redis
import time
from mirrcore.job_queue import JobQueue
from mirrcore.redis_check import is_redis_available
import json
import pandas as pd


class AttachmentsGenerator:
    '''
    TODO:
    * Need attachments in a csv file. --> This will be a mongoexport command once the system is taken down
    mongoexport --db=mirrulations --collection=comments --type=csv --fields=data.id,data.relationships.attachments.links.related --out=/home/cs334/capstone2022/attachments_list.csv

    * Iterate over that csv file to get the links from the entry

    * Create a new job with those links
    '''
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


    attachments_index = 0
    attachments_list = []

    # This is how the attachments generator was working during the last sprint
    data_frame = generator.read_attachments_csv()
    for link in data_frame['data.relationships.attachments.links.related']:
        attachments_list.append(link)

    for link in attachments_list:
        job = generator.add_job('data.relationships.attachments.links.related', link)
        attachments_index += 1

    '''
    # Would this work???
    for link in data_frame['data.relationships.attachments.links.related']:
        job = generator.add_job('attachments', link)
    '''

    database.lpush('jobs_waiting_queue', json.dumps(job))
