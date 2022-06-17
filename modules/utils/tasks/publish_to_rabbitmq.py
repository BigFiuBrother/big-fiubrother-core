from modules.events.big_fiubrother_core_events.message_clients import Publisher
from ...messages import encode_message
from . import QueueTask
import logging


class PublishToRabbitMQ(QueueTask):

    def __init__(self, configuration, input_queue):
        super().__init__(input_queue)
        self.configuration = configuration

    def init(self):
        super().init()
        self.publisher = Publisher(self.configuration)

    def execute_with(self, message):
        logging.info("RabbitMQPublisher message to publish: {}".format(message.id()))
        message = encode_message(message)
        self.publisher.publish(message)
