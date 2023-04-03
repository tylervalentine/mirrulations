class InvalidResultsException(Exception):
    """
    Raised when no results/json data are sent
    """
    message = {'error': 'The body does not contain the results'}
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


class NoJobsException(Exception):
    """
    Raised when no jobs are listed in the redis database
    """
    message = {'error': 'No jobs available'}
    status_code = 403


class NoJobsAvailableException(Exception):
    """
    Raises an Exception when there are no jobs available in the job queue.
    """

    def __init__(self, message="There are no jobs available"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
