from mirrclient.exceptions import MissingClientIDException
from mirrclient.exceptions import InvalidClientIDException


class GetJobValidator():
    """Validates the jobs sent by the client"""
    @classmethod
    def check_get_jobs(cls, client_id):
        # if data.get('jobs_waiting_queue') == 0:
        #     raise NoJobsException()
        if client_id is None:
            raise MissingClientIDException()
        if client_id.isdigit():
            client_id = int(client_id)
            if 0 < client_id:
                return True
        raise InvalidClientIDException()
