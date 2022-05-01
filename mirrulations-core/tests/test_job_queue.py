
from this import d
from fakeredis import FakeRedis
from mirrmock import mock_redis
from mirrmock.mock_redis import MockRedisWithStorage
from pytest import fixture
from mirrcore.job_queue import JobQueue

    
def test_first_job_added_with_id_0():
    database = FakeRedis()
    queue = JobQueue(database)

    queue.add_job('http://a.b.c')

    assert queue.get_num_jobs() == 1
    job = queue.get_job()
    assert job['job_id'] == 1
    assert job['url'] == 'http://a.b.c'
    

def test_job_added_with_next_id():
    database = FakeRedis()
    database.set('last_job_id', 42)
    queue = JobQueue(database)

    queue.add_job('http://a.b.c')

    assert queue.get_num_jobs() == 1
    job = queue.get_job()
    assert job['job_id'] == 43
    assert job['url'] == 'http://a.b.c'
    

def test_last_timestamp():

    database = FakeRedis()
    queue = JobQueue(database)

    assert queue.get_last_timestamp_string('dockets') == '1972-01-01 00:00:00'
    assert queue.get_last_timestamp_string('documents') == \
           '1972-01-01 00:00:00'
    assert queue.get_last_timestamp_string('comments') == '1972-01-01 00:00:00'

    queue.set_last_timestamp_string('dockets', '2010-06-10T20:49:03Z')
    queue.set_last_timestamp_string('documents', '2015-06-10T20:49:03Z')
    queue.set_last_timestamp_string('comments', '2020-06-10T20:49:03Z')

    assert queue.get_last_timestamp_string('dockets') == '2010-06-10 20:49:03'
    assert queue.get_last_timestamp_string('documents') == \
           '2015-06-10 20:49:03'
    assert queue.get_last_timestamp_string('comments') == '2020-06-10 20:49:03'

# @fixture(name='mock_redis')
# def fixture_MockRedisWithStorage():
#     return mock_redis.MockRedisWithStorage()

def test_increment_function():
    # with mock_redis:
    database = MockRedisWithStorage()
    queue = JobQueue(database)

    database.set('num_jobs_attachments_waiting', 0)
    database.set('num_jobs_comments_waiting', 0)
    print(database.data['num_jobs_comments_waiting'])
    database.set('num_jobs_documents_waiting', 0)
    database.set('num_jobs_dockets_waiting', 0)

    queue.add_job('http://a.b.c', 'comments')
    queue.add_job('http://a.b.c', 'documents')
    queue.add_job('http://a.b.c', 'dockets')
    queue.add_job('http://a.b.c', 'attachments')
    # database increments in add_job function
    assert database.get('num_jobs_comments_waiting') == 1
    assert database.get('num_jobs_documents_waiting') == 1
    assert database.get('num_jobs_dockets_waiting') == 1
    assert database.get('num_jobs_attachments_waiting') == 1

