import os


class PathGenerator:

    def __init__(self):
        self.path = "data"

    def get_path(self, job):
        if job['job_type'] == 'dockets':
            return get_docket_path(job)

    def get_docket_path(self, job): 
        job = job['data']
        job_id = job['id']
        agency, year, docket_id = job_id.split('-')
        return f'data/{agency}/{year}/{job_id}/text-{job_id}/docket/'
