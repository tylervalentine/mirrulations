
from c21server.work_gen.job_queue import JobQueue
from fakeredis import FakeRedis

def test_job_added_with_next_id():
    db = FakeRedis()

    q = JobQueue(db)

    q.add_job('http://a.b.c')

    assert q.get_num_jobs() == 1


