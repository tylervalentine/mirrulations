from c21server.work_gen.data_storage import DataStorage


class ResultsProcessor:

    def __init__(self, job_queue):
        self.job_queue = job_queue
        self.data_storage = DataStorage()

    def process_results(self, results_dict):
        for item in results_dict['data']:
            if not self.data_storage.exists(item):
                url = item['links']['self']
                self.job_queue.add_job(url)
