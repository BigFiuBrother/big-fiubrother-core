import threading
import pika

class QueueConsumerRabbitMq:

    def __init__(self, rabbitmqhost, consume_queue, consume_callback):

        # Create connection and channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmqhost))
        self.channel = self.connection.channel()

        # Set face detection job queue name
        self.consume_queue = consume_queue

        # Consume from queue
        self.channel.basic_consume(self._process_message, queue=self.consume_queue, no_ack=True)

        # Save consume callback
        self.consume_callback = consume_callback

        # Create thread
        self.thread = threading.Thread(target=self._start_consuming)

    def _process_message(self, ch, method, props, body):
        self.consume_callback(body)

    def _start_consuming(self):
        self.channel.start_consuming()

    def start(self):
        self.thread.start()

    def stop(self):
        self.channel.stop_consuming()
        self.thread.join()