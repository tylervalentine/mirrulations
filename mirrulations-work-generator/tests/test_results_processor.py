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


def test_one_job_is_added_if_not_a_comment():
    database = FakeRedis()
    results = MockDataSet(1, job_type='dockets').get_results()
    processor = ResultsProcessor(JobQueue(database), MockDataStorage())
    processor.process_results(json.loads(results[0]['text']))
    assert database.llen('jobs_waiting_queue') == 1


def test_adds_two_jobs_if_is_comment():
    database = FakeRedis()
    results = MockDataSet(1, job_type='comments').get_results()
    processor = ResultsProcessor(JobQueue(database), MockDataStorage())
    processor.process_results(json.loads(results[0]['text']))
    assert database.llen('jobs_waiting_queue') == 2


def test_job_types_added_if_comment_is_a_comment_type_and_attachment_type():
    database = FakeRedis()
    results = MockDataSet(1, job_type='comments').get_results()
    processor = ResultsProcessor(JobQueue(database), MockDataStorage())
    processor.process_results(json.loads(results[0]['text']))

    job_type_1 = database.lindex('jobs_waiting_queue', 0)
    job_type_2 = database.lindex('jobs_waiting_queue', 1)

    assert json.loads(job_type_1.decode())["job_type"] == "attachments"
    assert json.loads(job_type_2.decode())["job_type"] == "comments"
