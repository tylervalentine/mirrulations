
from fakeredis import FakeRedis
from c21server.work_gen.job_queue import JobQueue


def test_job_added_with_next_id():
    database = FakeRedis()

    queue = JobQueue(database)

    queue.add_job('http://a.b.c')

    assert queue.get_num_jobs() == 1
