from ...message_clients.rabbitmq import Consumer
from ...messages import decode_message
from . import Input
from queue import Queue
import threading


class RabbitMQConsumer(Input):

    def __init__(self, configuration):
        self.configuration = configuration
        
        self._processed_messages = Queue()
        self._thread = threading.Thread(target=self._start_consumer)
        self._thread.start()

    def _start_consumer(self):
        self.consumer = Consumer(self.configuration, self._process_message)
        self.consumer.run()
        
    def poll(self):
        return self._processed_messages.get()

    def stop(self):
        self.consumer.stop()
        self._thread.join()
        self._processed_messages.put(None)

    def _process_message(self, body):
        self._processed_messages.put(decode_message(body))
