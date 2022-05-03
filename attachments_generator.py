import redis
import time
from mirrcore.job_queue import JobQueue
from mirrcore.redis_check import is_redis_available
import pandas as pd

'''
MongoExport command that needs to be run once we take down the system. This is a one time command:

mongoexport --db=mirrulations --collection=comments --type=csv --fields=data.id,data.attributes.agencyId,data.relationships.attachments.links.related --out=/home/cs334/capstone2022/attachments_list.csv
'''

class AttachmentsGenerator:
    def read_attachments_csv(self):
        data_frame = pd.read_csv('/home/cs334/capstone2022/mirrulations-core/tests/test_put_files', usecols=['data.id',
                'data.attributes.agencyId', 'data.relationships.attachments.links.related'], 
                dtype={'data.id':'str', 'data.attributes.agency_id':'str',
                'data.relationships.attachments.links.related':'str'})
        return data_frame

    def __init__(self, job_queue, database):
        self.job_queue = job_queue
        self.database = database

    def get_job_id(self):
        job_id = self.database.incr('last_job_id')
        return job_id


if __name__ == '__main__':
    database = redis.Redis()
    while not is_redis_available(database):
        print("Redis database is busy loading")
        time.sleep(30)

    job_queue = JobQueue(database)
    generator = AttachmentsGenerator(job_queue, database)


    data_frame = generator.read_attachments_csv()

    for link, agency, regulations_id in zip(data_frame['data.relationships.attachments.links.related'], data_frame['data.attributes.agencyId'], data_frame['data.id']):
        print(link, agency, regulations_id)
        job_queue.add_job(link, job_type='attachments', reg_id=regulations_id, agency=agency)