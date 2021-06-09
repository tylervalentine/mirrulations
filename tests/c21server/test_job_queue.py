
from fakeredis import FakeRedis
from c21server.work_gen.job_queue import JobQueue


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
