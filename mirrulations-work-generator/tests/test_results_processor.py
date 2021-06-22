import json
import os
from fakeredis import FakeRedis
from mirrgen.results_processor import ResultsProcessor
from mirrcore.job_queue import JobQueue
from mirrmock.mock_data_storage import MockDataStorage


def test_process_results():
    database = FakeRedis()

    dir_path = os.path.dirname(os.path.realpath(__file__))

    processor = ResultsProcessor(JobQueue(database), MockDataStorage())
    data = open(f'{dir_path}/data/dockets_listing.json').read()
    processor.process_results(json.loads(data))

    assert database.llen('jobs_waiting_queue') == 10
