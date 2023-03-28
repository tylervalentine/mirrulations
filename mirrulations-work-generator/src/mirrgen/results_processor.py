import os
from collections import Counter
from mirrcore.path_generator import PathGenerator


def result_exists(search_element):
    path_generator = PathGenerator()
    # We are checking search results, but the PathGenerator expects
    # the actual data of a docket, document, or comment JSON.
    # But the PathGenerator only needs to type, agency, and other
    # data that is in the search results.  Therefore, we can simply
    # wrap the search result in a data field and then use the PathGenerator.
    fake_result = {'data': search_element}
    the_path = path_generator.get_path(fake_result)
    return os.path.exists(the_path)


class ResultsProcessor:

    def __init__(self, job_queue):
        self.job_queue = job_queue

    def process_results(self, results_dict):
        counts = Counter()
        for item in results_dict['data']:
            if not result_exists(item):
                # sets url and job_type
                url = item['links']['self']
                job_type = item['type']
                if job_type == 'comments':
                    # updates the url and job_type
                    url = url + '?include=attachments'
                # adds current job to jobs_waiting_queue
                self.job_queue.add_job(url, job_type)
                counts[job_type] += 1
            else:
                counts['preexisting'] += 1
        print_report(counts)


def print_report(counts):
    # join counts into a single string
    report = ', '.join([f'{key}: {counts[key]}' for key in counts])
    print(f'Added {report}')
