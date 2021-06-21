
from fakeredis import FakeRedis
from mirrgen.job_queue import JobQueue


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
