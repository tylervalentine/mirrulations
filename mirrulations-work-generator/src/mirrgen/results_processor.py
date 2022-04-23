
class ResultsProcessor:

    def __init__(self, job_queue, data_storage):
        self.job_queue = job_queue
        self.data_storage = data_storage

    def process_results(self, results_dict):
        for item in results_dict['data']:
            if not self.data_storage.exists(item):
                url = item['links']['self']
                job_type = item['type']
                has_attachment = 'relationships' in item
                if job_type == 'comments' and has_attachment == True:
                    self.job_queue.add_job(url, job_type)
                    relatsh = 'relationships'
                    attm = 'attachments'
                    url = item[relatsh][attm]['links']['related']
                    job_type = 'attachments'
                self.job_queue.add_job(url, job_type)
