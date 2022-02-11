import os
import time
import dotenv
import redis
from mirrgen.search_iterator import SearchIterator
from mirrgen.results_processor import ResultsProcessor
from mirrcore.regulations_api import RegulationsAPI
from mirrcore.job_queue import JobQueue
from mirrcore.data_storage import DataStorage


class WorkGenerator:

    def __init__(self, job_queue, api, datastorage):
        self.job_queue = job_queue
        self.api = api
        self.processor = ResultsProcessor(job_queue, datastorage)

    def download(self, endpoint):
        last_timestamp = self.job_queue.get_last_timestamp_string(endpoint)
        for result in SearchIterator(self.api, endpoint, last_timestamp):
            if result == {}:
                continue
            self.processor.process_results(result)
            timestamp = result['data'][-1]['attributes']['lastModifiedDate']
            self.job_queue.set_last_timestamp_string(endpoint, timestamp)


if __name__ == '__main__':

    def is_redis_available(database):
        try:
            # return fakeredis.FakeRedis('localhost').ping() # Not sure if the database is at localhost or 'redis'
            return database.ping() # Not sure if the database is at localhost or 'redis'
        except (ConnectionRefusedError, redis.BusyLoadingError) as error:
            return False

    # I wrapped the code in a function to avoid pylint errors
    # about shadowing api and job_queue
    def generate_work():
        dotenv.load_dotenv()
        api = RegulationsAPI(os.getenv('API_KEY'))

        database = redis.Redis('redis')
        
        while not is_redis_available(database):
            print("error")
            time.sleep(30)


        job_queue = JobQueue(database)

        storage = DataStorage()

        generator = WorkGenerator(job_queue, api, storage)

        generator.download('dockets')
        generator.download('documents')
        generator.download('comments')

    while True:
        generate_work()
        # sleep 6 hours
        time.sleep(60 * 60 * 6)
