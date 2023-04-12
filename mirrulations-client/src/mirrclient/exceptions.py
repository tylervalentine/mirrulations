class NoJobsAvailableException(Exception):
    """
    Raises an Exception when there are no jobs available in the job queue.
    """

class APITimeoutException(Exception):
    """
    Raises an Exception when the regulations.gov API
    does not respond in time.
    """
