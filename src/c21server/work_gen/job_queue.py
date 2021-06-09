
class JobQueue:

    def __init__(self, db):
        self.db = db

    def add_job(self, job):
        self.db.lpush('jobs_waiting_queue', job)

    def get_num_jobs(self):
        return self.db.llen('jobs_waiting_queue')

