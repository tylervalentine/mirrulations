from mirrserver.exceptions import MissingClientIDException
from mirrserver.exceptions import InvalidClientIDException


class GetJobValidator():
    """Validates the jobs sent by the client"""
    def check_get_jobs(self, client_id):
        # if data.get('jobs_waiting_queue') == 0:
        #     raise NoJobsException()
        if client_id is None:
            raise MissingClientIDException()
        if client_id.isdigit() or isinstance(client_id, int):
            client_id = int(client_id)
            if 0 < client_id < 20:
                return True
        raise InvalidClientIDException()
