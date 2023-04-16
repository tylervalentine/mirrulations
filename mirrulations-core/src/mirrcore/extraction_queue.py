import os
from mirrcore.rabbitmq import RabbitMQ


class ExtractionQueue:
    """
    This class is an abstraction of the process of adding and
    getting attachment paths from the underlying attachment queue.
    It hides the implementation details of how extractions are
    stored in queue.
    """

    def __init__(self):
        self.rabbitmq = RabbitMQ('extraction_queue')

    def add(self, path):
        """
        Add a path of an attachment to extract to the queue.
        If the path is not a string, or the path does not actually match
        up with a file, then the path is not added to the queue.
        @param path: the absolute path of the attachment to extract
        """
        if not isinstance(path, str):
            return
        if not os.path.isfile(path):
            return
        self.rabbitmq.add(path)

    def size(self):
        """
        @return the number of attachments in the queue
        """
        return self.rabbitmq.size()

    def get(self):
        """
        @return the next attachment path in the queue,
            or None if the queue is empty
        """
        return self.rabbitmq.get() if self.size() != 0 else None
