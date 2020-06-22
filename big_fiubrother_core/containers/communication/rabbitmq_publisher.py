from ...message_clients.rabbitmq import Publisher
from ...messages import encode_message
from . import Output


class RabbitMQPublisher(Output):

    def __init__(self, configuration):
        self.configuration = configuration

    def init(self):
        self.publisher = Publisher(self.configuration)

    def send(self, message):
        self.publisher.publish(encode_message(message))
