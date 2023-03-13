class JobQueueException(Exception):
    """
    Raised when the job queue has an exception occur.
    503 error defined as not able to connect to service
    """
    message = {'error': 'The job queue encountered an error'}
    status_code = 503
