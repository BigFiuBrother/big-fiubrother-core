import pika

class QueuePublisher:

    def __init__(self, rabbitmqhost, publish_queue):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmqhost))
        self.channel = self.connection.channel()

        self.publish_queue = publish_queue

    def publish(self, message_bytes):
        self.channel.basic_publish("", self.publish_queue, message_bytes)
