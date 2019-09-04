import pika


class QueueConsumer:

    def __init__(self, rabbitmqhost, consume_queue, consume_callback):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmqhost))
        self.channel = self.connection.channel()
        self.consume_callback = consume_callback

        self.channel.basic_consume(queue=consume_queue, on_message_callback=self._process_message)
    
    def start(self):
        self.channel.start_consuming()

    def stop(self):
        self.channel.stop_consuming()
    
    def _process_message(self, ch, method, props, body):
        self.consume_callback(body)