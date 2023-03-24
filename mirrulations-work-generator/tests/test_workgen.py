from fakeredis import FakeRedis
from mirrcore.job_queue import JobQueue
from mirrcore.regulations_api import RegulationsAPI
from mirrmock.mock_dataset import MockDataSet
from mirrmock.mock_data_storage import MockDataStorage
from mirrmock.mock_rabbitmq import MockRabbit
from mirrgen.work_generator import WorkGenerator


def test_work_generator_single_page(requests_mock, mocker):
    mocker.patch('time.sleep')
    results = MockDataSet(150).get_results()
    requests_mock.get('https://api.regulations.gov/v4/documents', results)

    database = FakeRedis()
    api = RegulationsAPI('FAKE_KEY')
    job_queue = JobQueue(database)
    # mock out the rabbit connection
    job_queue.rabbitmq = MockRabbit()

    storage = MockDataStorage()

    generator = WorkGenerator(job_queue, api, storage)
    generator.download('documents')

    assert job_queue.get_num_jobs() == 150


def test_work_generator_large(requests_mock, mocker):
    mocker.patch('time.sleep')
    results = MockDataSet(6666).get_results()
    requests_mock.get('https://api.regulations.gov/v4/documents', results)

    database = FakeRedis()
    api = RegulationsAPI('FAKE_KEY')
    job_queue = JobQueue(database)
    # mock out the rabbit connection
    job_queue.rabbitmq = MockRabbit()

    storage = MockDataStorage()
    generator = WorkGenerator(job_queue, api, storage)
    generator.download('documents')

    assert job_queue.get_num_jobs() == 6666


def test_work_generator_retries_after_500(requests_mock, mocker):
    mocker.patch('time.sleep')
    results = MockDataSet(150).get_results()
    results.insert(0, {'json': '{}', 'status_code': 500})
    requests_mock.get('https://api.regulations.gov/v4/documents', results)

    database = FakeRedis()
    api = RegulationsAPI('FAKE_KEY')
    job_queue = JobQueue(database)
    # mock out the rabbit connection
    job_queue.rabbitmq = MockRabbit()

    storage = MockDataStorage()
    generator = WorkGenerator(job_queue, api, storage)
    generator.download('documents')

    assert len(requests_mock.request_history) == 2


def test_work_generator_output_after_500_error(capsys, requests_mock, mocker):
    mocker.patch('time.sleep')
    results = MockDataSet(150).get_results()
    results.insert(0, {'json': '{}', 'status_code': 504})
    requests_mock.get('https://api.regulations.gov/v4/documents', results)

    api = RegulationsAPI('FAKE_KEY')
    job_queue = JobQueue(FakeRedis())
    # mock out the rabbit connection
    job_queue.rabbitmq = MockRabbit()

    generator = WorkGenerator(job_queue, api, MockDataStorage())
    generator.download('documents')

    print_data = [
        'FAILED: https://api.regulations.gov/v4/documents\n',
        '504 Server Error from url ',
        'https://api.regulations.gov/v4/documents?sort=',
        'lastModifiedDatepage[size]=250filter[lastModifiedDate]',
        '[ge]=1971-12-31+19:00:00page[number]=1\n',
        'Added any: 150\n'
    ]
    assert capsys.readouterr().out == "".join(print_data)
