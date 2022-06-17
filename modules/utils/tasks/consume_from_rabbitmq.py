from modules.events.big_fiubrother_core_events.message_clients import Consumer
from ...messages import decode_message
from . import Task
import logging


class ConsumeFromRabbitMQ(Task):

    def __init__(self, configuration, output_queue):
        self.configuration = configuration
        self.output_queue = output_queue

    def init(self):
        super().init()
        self.consumer = Consumer(self.configuration, self._consumer_callback)

    def execute(self):
        self.consumer.start()

    def stop(self):
        super().stop()
        self.consumer.stop()

    def _consumer_callback(self, body):
        message = decode_message(body)
        logging.info("RabbitMQConsumer fetched message: {}".format(message.id()))
        self.output_queue.put(message)
