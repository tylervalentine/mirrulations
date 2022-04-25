
class ResultsProcessor:

    def __init__(self, job_queue, data_storage):
        self.job_queue = job_queue
        self.data_storage = data_storage

    def process_results(self, results_dict):
        for item in results_dict['data']:
            if not self.data_storage.exists(item):
                # sets url and job_type
                url = item['links']['self']
                job_type = item['type']
                # adds current job to jobs_waiting_queue
                self.job_queue.add_job(url, job_type)
                # checks to see if it has an attachment
                has_attachment = 'relationships' in item
                if job_type == 'comments' and has_attachment is True:
                    relatsh = 'relationships'
                    attm = 'attachments'
                    # updates the url and job_type
                    url = item[relatsh][attm]['links']['related']
                    job_type = 'attachments'
                    # adds new attachment job to jobs_waiting_queue
                    self.job_queue.add_job(url, job_type)
