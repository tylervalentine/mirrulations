from mirrmock.mock_rabbitmq import MockRabbit
from mirrcore.extraction_queue import ExtractionQueue


def test_add_good_path(mocker):
    mocker.patch('os.path.isfile', return_value=True)

    queue = ExtractionQueue()
    queue.rabbitmq = MockRabbit()

    queue.add('test')

    assert queue.size() == 1
    assert queue.get() == 'test'


def test_add_bad_path():
    queue = ExtractionQueue()
    queue.rabbitmq = MockRabbit()

    queue.add('test')

    assert queue.size() == 0
    assert queue.get() is None
