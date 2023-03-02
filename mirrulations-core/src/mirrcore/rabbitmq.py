import pika
import json


def make_channel():
    """
    Connections timeout, so we have to create a new one each time we interact
    with RabbitMQ

    @return: a new channel connected to the jobs_waiting_queue
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare('jobs_waiting_queue')
    return channel


class RabbitMQ:
    """
    Encapsulate calls to RabbitMQ in one place
    """
    def add(self, job):
        """
        Add a job to the channel
        @param job: the job to add
        @return: None
        """
        channel = make_channel()
        channel.basic_publish(exchange='',
                              routing_key='jobs_waiting_queue',
                              body=json.dumps(job))

    def size(self):
        """
        Get the number of jobs in the queue
        @return: a non-negative integer
        """
        channel = make_channel()
        queue = channel.queue_declare('jobs_waiting_queue')
        return queue.method.message_count

    def get(self):
        """
        Take one job from the queue and return it
        @return: a job, or None if there are no jobs
        """
        # Connections timeout, so we have to create a new one each time
        channel = make_channel()
        method_frame, header_frame, body = channel.basic_get('jobs_waiting_queue')
        # If there was no job available
        if method_frame is None:
            return None

        channel.basic_ack(method_frame.delivery_tag)
        return json.loads(body.decode('utf-8'))
