from ..message_clients.rabbitmq import Publisher
from ..messages import encode_message
from . import Task


class PublishToRabbitMQ(Task):

    def __init__(self, configuration):
        self.publisher = Publisher(configuration)

    def execute(self, message):
        self.publisher.publish(encode_message(message))
