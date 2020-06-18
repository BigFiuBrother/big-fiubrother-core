from ..message_clients.rabbitmq import Consumer
from ..messages import decode_message
from . import Task
from queue import Queue


class ConsumeFromRabbitMQ(Task):

    def __init__(self, configuration):
        self.consumer = Consumer(configuration, self._process_message)
        self._processed_messages = Queue()

    def init(self):
        self.consumer.start()

    def execute(self):
        return self._processed_messages.get()

    def close(self):
        self.consumer.stop()

    def _process_message(self, body):
        self._processed_messages.put(decode_message(body))
