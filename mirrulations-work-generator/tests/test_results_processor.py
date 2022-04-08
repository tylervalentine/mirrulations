import json
import os
from fakeredis import FakeRedis
from mirrgen.results_processor import ResultsProcessor
from mirrcore.job_queue import JobQueue
from mirrmock.mock_data_storage import MockDataStorage
from mirrmock.mock_dataset import MockDataSet


def test_process_results():
    database = FakeRedis()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    processor = ResultsProcessor(JobQueue(database), MockDataStorage())
    with open(f'{dir_path}/data/dockets_listing.json',
              encoding='utf8') as listings:
        data = listings.read()
        processor.process_results(json.loads(data))

    assert database.llen('jobs_waiting_queue') == 10


def test_adds_two_jobs_if_is_comment():
    database = FakeRedis()
    results = MockDataSet(1, job_type='comments').get_results()
    processor = ResultsProcessor(JobQueue(database), MockDataStorage())
    processor.process_results(json.loads(results[0]['text']))
    assert database.llen('jobs_waiting_queue') == 2

