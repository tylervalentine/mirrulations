import json
from fakeredis import FakeRedis
from c21server.work_gen.results_processor import ResultsProcessor
from c21server.work_gen.job_queue import JobQueue


def test_process_results():
    database = FakeRedis()

    processor = ResultsProcessor(JobQueue(database))
    data = open('tests/data/dockets_listing.json').read()
    processor.process_results(json.loads(data))

    assert database.llen('jobs_waiting_queue') == 10
