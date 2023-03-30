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
                    self.unfound_jobs[res['type']] = res['links']['self']
                    print(f"Finished adding {res['id']} to file")
                    counter['Not_in_db'] += 1
                else:
                    print(f"{res['id']} exists in database")
                counter['Total_validated'] += 1
            print(f'Jobs not found in database: {counter["Not_in_db"]}')
            print(f'Total jobs validated: {counter["Total_validated"]}')
            percentage = (counter['Total_validated'] / collection_size) * 100
            print(f'{percentage:.2f}%')
            time.sleep(3.6)


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
    # Write unfound jobs to JSON file
    unfound_jobs_object = json.dumps(generator.unfound_jobs)

    with open("unfound_jobs.json", "w", encoding="utf-8") as outfile:
        outfile.write(unfound_jobs_object)


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
