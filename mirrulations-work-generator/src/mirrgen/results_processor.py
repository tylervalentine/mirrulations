
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
                regulation_id = item['id']
                agency = item['attributes']['agencyId']
                # adds current job to jobs_waiting_queue
                self.job_queue.add_job(url, job_type, regulation_id, agency)
                if job_type == 'comments':
                    # updates the url and job_type
                    url = url + '/attachments'
                    job_type = 'attachments'
                    regulation_id = item['id']
                    agency = item['attributes']['agencyId']
                    # adds new attachment job to jobs_waiting_queue
                    self.job_queue.add_job(url, job_type, regulation_id, agency)
