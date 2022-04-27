import redis
import time
from mirrcore.job_queue import JobQueue
from mirrcore.redis_check import is_redis_available
import json
import pandas as pd
import sys

'''
MongoExport command that needs to be run once we take down the system. This is a one time command:

mongoexport --db=mirrulations --collection=comments --type=csv --fields=data.id,data.attributes.agencyId,data.relationships.attachments.links.related --out=/home/cs334/capstone2022/attachments_list.csv
'''



class AttachmentsGenerator:
    def read_attachments_csv():
        data_frame = pd.read_csv('/home/cs334/capstone2022/attachments_list.csv', usecols=['data.id',
                'data.attributes.agency_id', 'data.relationships.attachments.links.related'], 
                dtype={'data.id':'str', 'data.attributes.agency_id':'str',
                'data.relationships.attachments.links.related':'str'})
        return data_frame

    def __init__(self, job_queue, database):
        self.job_queue = job_queue
        self.database = database

    def get_job_id(self):
        job_id = self.database.incr('last_job_id')
        return job_id

    def add_job(self, job_type, url, regulations_id, agency_id):
        job_id = self.get_job_id()
        if job_type == 'attachments':
            job = {'job_id': job_id,
                    'url': url,
                    'job_type': job_type,
                    'regulations_id': regulations_id,
                    'agency_id': agency_id
                }
            return job

if __name__ == '__main__':
    database = redis.Redis()
    while not is_redis_available(database):
        print("Redis database is busy loading")
        time.sleep(30)

    job_queue = JobQueue(database)
    generator = AttachmentsGenerator(job_queue, database)

    limit = 1000000000
    attachments_list = []
    agency_list = []
    regulations_id_list = []
    counter = 0

    # This is how the attachments generator was working during the last sprint
    data_frame = generator.read_attachments_csv()

    for link in data_frame['data.relationships.attachments.links.related']:
        attachments_list.append(link)

    for agency_id in data_frame['data.attributes.agency_id']:
        agency_list.append(agency_id)

    for regulations_id in data_frame['data.id']:
        agency_list.append(regulations_id)


    with open("last_index.txt", "r") as file:
        last_link_index = file.readline()

    with open("last_index.txt", "w") as file:
        for link in attachments_list[int(last_link_index): ]:
            for agency_id in agency_list[int(last_link_index)]:
                for regulations_id in regulations_id_list[int(last_link_index)]:

                    if counter > limit:
                        sys.exit()

                    elif counter < limit:
                        job = generator.add_job('data.relationships.attachments.links.related', link, regulations_id, agency_id)
                        counter += 1
                        if link == attachments_list[-1]:
                            file.write(str(0))

                    elif counter == limit:
                        file.write(str(attachments_list.index(link)))
                        counter += 1

    database.lpush('jobs_waiting_queue', json.dumps(job))
