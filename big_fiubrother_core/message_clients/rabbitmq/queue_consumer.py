import threading
import pika

class QueueConsumer:

    def __init__(self, rabbitmqhost, consume_queue, consume_callback):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmqhost))
        self.channel = self.connection.channel()

        self.consume_queue = consume_queue

        self.channel.basic_consume(self._process_message, queue=self.consume_queue, no_ack=True)

        self.consume_callback = consume_callback

        # Create thread to consume
        self._thread = threading.Thread(target=self._start_consuming)

    def _process_message(self, ch, method, props, body):
        self.consume_callback(body)

    def _start_consuming(self):
        self.channel.start_consuming()

    def start(self):
        self._thread.start()

    def stop(self, wait=False):
        self.channel.stop_consuming()

        if wait:
            self.wait_until_stopped()

    def wait_until_stopped(self):
        self._thread.join()