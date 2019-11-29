import pika


class Consumer:

    def __init__(self, configuration, consume_callback):
        self.host = configuration['host']
        self.queue = configuration['queue']
        self.consume_callback = consume_callback

        self.credentials = pika.PlainCredentials(
            configuration['username'], configuration['password'])
        self.parameters = pika.ConnectionParameters(
            host=self.host, credentials=self.credentials)

        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self._process_message)

    def start(self):
        self.channel.start_consuming()

    def stop(self):
        self.channel.stop_consuming()

    def _process_message(self, ch, method, props, body):
        self.consume_callback(body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
