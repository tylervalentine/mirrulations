import os
import sys
import time
from collections import Counter
import json
from dotenv import load_dotenv
import redis
from mirrgen.search_iterator import SearchIterator
from mirrcore.redis_check import is_redis_available
from mirrcore.regulations_api import RegulationsAPI
from mirrcore.data_storage import DataStorage


class Validator:

    def __init__(self, api, datastorage):
        self.api = api
        self.datastorage = datastorage
        self.unfound_jobs = {}

    def download(self, endpoint):
        beginning_timestamp = '1972-01-01 00:00:00'
        collection_size = self.datastorage.get_collection_size(endpoint)
        counter = Counter()
        for result in SearchIterator(self.api, endpoint, beginning_timestamp):
            if result == {}:
                continue
            for res in result['data']:
                if not self.datastorage.exists(res):
                    print(f"{res['id']} not in database, writing to file")
                    write_unfound_jobs(res, self.unfound_jobs)
                    time.sleep(3.6)
                    counter['Not_in_db'] += 1
                else:
                    print(f"{res['id']} exists in database")
                counter['Total_validated'] += 1
            print(f'Jobs not found in database: {counter["Not_in_db"]} \n \
            Total jobs validated: {counter["Total_validated"]} \n \
            Percentage of jobs validated: \
                {counter["Total_validated"] / collection_size * 100}%')


def write_unfound_jobs(res, unfound_jobs):
    if res['type'] not in unfound_jobs:
        unfound_jobs[f"missing_{res['type']}"] = [res['links']['self']]
    else:
        unfound_jobs[f"missing_{res['type']}"].append(
            res['links']['self'])
    with open("validator/unfound_jobs.json", "w+",
              encoding="utf-8") as outfile:
        json.dump(unfound_jobs, outfile, indent=4)


def generate_work(collection=None):

    database = redis.Redis('redis')
    # Sleep for 30 seconds to give time to load
    while not is_redis_available(database):
        print("Redis database is busy loading")
        time.sleep(30)
    # Get API key
    load_dotenv()
    api = RegulationsAPI(os.getenv("API_KEY"))
    # Download using validator
    storage = DataStorage()
    generator = Validator(api, storage)
    if not collection:
        generator.download('dockets')
        generator.download('documents')
        generator.download('comments')
    else:
        generator.download(collection)


if __name__ == '__main__':
    job_types = ('dockets', 'documents', 'comments')
    while True:
        # Start from last job type performed
        if len(sys.argv) > 1 and sys.argv[1] in job_types:
            generate_work(sys.argv[1])
        else:
            generate_work()
        print("Validator sleeping for 30 days...")
        time.sleep(60*60*24*30)
