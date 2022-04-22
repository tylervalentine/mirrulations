import json
#from mirrcore import redis_queue_utils
class JobQueue:

    def __init__(self, database):
        self.database = database

    def add_job(self, url, job_type=None):
        job_id = self.get_job_id()
        job = {
            'job_id': job_id,
            'url': url,
            'job_type': job_type
            }
        self.database.lpush('jobs_waiting_queue', json.dumps(job))
        # reflect change to the queue len in redis db to avoid timeouts from counting true len
        if job_type == 'attachments':
            self.get_attachment_counter
        elif job_type == 'comments':
            self.get_comment_counter
        elif job_type == 'documents':
            self.get_document_counter
        elif job_type == 'dockets':
            self.get_docket_counter
        
        

    def get_num_jobs(self):
        return self.database.llen('jobs_waiting_queue')
    
    def get_job(self):
        return json.loads(self.database.lpop('jobs_waiting_queue'))

    def get_job_id(self):
        job_id = self.database.incr('last_job_id')
        return job_id

    def get_attachment_counter(self):
        counter = self.database.incr('num_jobs_attachments_waiting')
        return counter
    
    def get_comment_counter(self):
        counter = self.database.incr('num_jobs_comments_waiting')
        return counter

    def get_document_counter(self):
        counter = self.database.incr('num_jobs_documents_waiting')
        return counter

    def get_docket_counter(self):
        counter = self.database.incr('num_jobs_dockets_waiting')
        return counter

    def get_last_timestamp_string(self, endpoint):
        key = f'{endpoint}_last_timestamp'
        if self.database.exists(key):
            return self.database.get(key).decode()
        return '1972-01-01 00:00:00'

    def set_last_timestamp_string(self, endpoint, date_string):
        key = f'{endpoint}_last_timestamp'
        self.database.set(key, date_string.replace('T', ' ')
                          .replace('Z', ''))

   