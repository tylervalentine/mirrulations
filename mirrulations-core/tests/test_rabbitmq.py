from unittest.mock import MagicMock

from mirrcore.rabbitmq import RabbitMQ
import pika

"""
This test exists to increase coverage.  The RabbitMQ class encapsulates
interactions with RabbitMQ.  We don't need to test the pika class,
so this test simply calls all the methods using a mock
"""


class ChannelSpy:

    def queue_declare(self, queue):
        return MagicMock()

    def basic_publish(self, exchange, routing_key, body):
        pass

    def basic_get(self, name):
        return None, None, None


class PikaSpy:

    def __init__(self, params):
        pass

    def channel(self):
        return ChannelSpy()


def test_rabbit_interactions(monkeypatch):

    monkeypatch.setattr(pika, 'BlockingConnection', PikaSpy)

    r = RabbitMQ()
    r.add('foo')
    r.size()
    r.get()
