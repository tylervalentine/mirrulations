
class ResultsProcessor:

    def __init__(self, job_queue):
        self.job_queue = job_queue

    def process_results(self, results_dict):
        for item in results_dict['data']:
            url = item['links']['self']
            self.job_queue.add_job(url)
