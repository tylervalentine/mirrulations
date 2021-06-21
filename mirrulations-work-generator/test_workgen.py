from fakeredis import FakeRedis
from c21server.work_gen.job_queue import JobQueue
from c21server.work_gen.work_generator import WorkGenerator
from c21server.work_gen.regulations_api import RegulationsAPI
from c21server.work_gen.mock_dataset import MockDataSet
from c21server.work_gen.mock_data_storage import MockDataStorage


def test_work_generator_single_page(requests_mock, mocker):
    mocker.patch('time.sleep')
    results = MockDataSet(150).get_results()
    requests_mock.get('https://api.regulations.gov/v4/documents', results)

    database = FakeRedis()
    api = RegulationsAPI('FAKE_KEY')
    job_queue = JobQueue(database)

    storage = MockDataStorage()

    generator = WorkGenerator(job_queue, api, storage)
    generator.download('documents')

    assert database.llen('jobs_waiting_queue') == 150


def test_work_generator_large(requests_mock, mocker):
    mocker.patch('time.sleep')
    results = MockDataSet(6666).get_results()
    requests_mock.get('https://api.regulations.gov/v4/documents', results)

    database = FakeRedis()
    api = RegulationsAPI('FAKE_KEY')
    job_queue = JobQueue(database)

    storage = MockDataStorage()
    generator = WorkGenerator(job_queue, api, storage)
    generator.download('documents')

    assert database.llen('jobs_waiting_queue') == 6666
