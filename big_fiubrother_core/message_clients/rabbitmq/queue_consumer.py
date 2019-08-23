import threading
import pika
from big_fiubrother_core.stoppable_thread import StoppableThread


class QueueConsumer(StoppableThread):

    def __init__(self, rabbitmqhost, consume_queue, consume_callback):
        super().__init__()

        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmqhost))
        self.channel = self.connection.channel()

        self.consume_queue = consume_queue

        self.channel.basic_consume(self._process_message, queue=self.consume_queue, no_ack=True)

        self.consume_callback = consume_callback
    
    def stop(self):
        super().stop()
        self.channel.stop_consuming()
    
    def _process_message(self, ch, method, props, body):
        self.consume_callback(body)

    def _execute(self):
        self.channel.start_consuming()


