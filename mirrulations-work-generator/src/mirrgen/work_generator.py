import os
import time
import dotenv
import redis
from mirrgen.search_iterator import SearchIterator
from mirrgen.results_processor import ResultsProcessor
from mirrgen.regulations_api import RegulationsAPI
from mirrgen.job_queue import JobQueue
from mirrgen.data_storage import DataStorage


class WorkGenerator:

    def __init__(self, job_queue, api, datastorage):
        self.job_queue = job_queue
        self.api = api
        self.processor = ResultsProcessor(job_queue, datastorage)

    def download(self, endpoint):
        last_timestamp = self.job_queue.get_last_timestamp_string(endpoint)
        for result in SearchIterator(self.api, endpoint, last_timestamp):
            self.processor.process_results(result)
            timestamp = result['data'][-1]['attributes']['lastModifiedDate']
            self.job_queue.set_last_timestamp_string(endpoint, timestamp)


if __name__ == '__main__':
    # I wrapped the code in a function to avoid pylint errors
    # about shadowing api and job_queue
    def generate_work():
        dotenv.load_dotenv()
        api = RegulationsAPI(os.getenv('API_KEY'))

        # Sleep to allow Redis to come online
        time.sleep(10)
        database = redis.Redis('redis')
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
