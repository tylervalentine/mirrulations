
class JobQueue:

    def __init__(self, database):
        self.database = database

    def add_job(self, job):
        self.database.lpush('jobs_waiting_queue', job)

    def get_num_jobs(self):
        return self.database.llen('jobs_waiting_queue')
