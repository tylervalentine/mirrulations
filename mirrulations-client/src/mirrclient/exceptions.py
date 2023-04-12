class NoJobsAvailableException(Exception):
    """
    Raises an Exception when there are no jobs available in the job queue.
    """
    def __init__(self, message="There are no jobs available"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'
