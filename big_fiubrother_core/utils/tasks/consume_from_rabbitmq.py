from ...message_clients.rabbitmq import Consumer
from ...messages import decode_message
from . import Task


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
        self.output_queue.put(decode_message(body))
