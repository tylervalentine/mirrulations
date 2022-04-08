class NoJobsException(Exception):
    """
    Raised when no jobs are listed in the redis database
    """
    message = {'error': 'No jobs available'}
    status_code = 403


class InvalidClientIDException(Exception):
    """
    Raised when the client ID is invalid
    (not 0<=client_id<20 or not an integer)
    """
    message = {'error': 'Invalid client ID'}
    status_code = 401


class MissingClientIDException(Exception):
    """
    Raised when the client ID is missing
    """
    message = {'error': 'Client ID was not provided'}
    status_code = 401


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
