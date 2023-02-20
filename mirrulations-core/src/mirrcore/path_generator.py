import os


class PathGenerator:

    def __init__(self):
        self.path = "data"

    def get_docket_path(self, job): 
        job = job['data']
        job_id = job['id']
        if "FRDOC" in job_id:
            agency, FRDOC, docket_num = job_id.split("_")
            docket_id = '_'.join([agency, FRDOC, docket_num])
            return f'data/{agency}/FRDOCS/{docket_id}/text-{docket_id}/docket/'

        agency, year, docket_id = job_id.split('-')
        return f'data/{agency}/{year}/{job_id}/text-{job_id}/docket/'


    def get_document_path(self, job):
        job = job['data']
        job_id = job['id']
        if "FRDOC" in job_id:
            agency, FRDOC, rest_of_id = job_id.split("_")
            docket_id, document_id = rest_of_id.split("-")
            docket_id = '_'.join([agency, FRDOC, docket_id])
            return f'data/{agency}/FRDOCS/{docket_id}/text-{docket_id}/documents/'

        agency, year, docket_id = job_id.split('-')
        return f'data/{agency}/{year}/{job_id}/text-{job_id}/docket/'

    def get_path(self, job):
        if job['job_type'] == 'dockets':
            return get_docket_path(job)
        if job['job_type'] == "documents":
            return get_document_path(job)
