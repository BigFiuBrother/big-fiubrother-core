import pika


class QueuePublisherRabbitMq:

    def __init__(self, rabbitmqhost, publish_queue):

        # Create connection and channel
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=rabbitmqhost))
        self.channel = self.connection.channel()

        # Set publish_queue name
        self.publish_queue = publish_queue

    def start(self):
        pass

    def stop(self):
        pass

    def publish(self, message_bytes):
        self.channel.basic_publish("", self.publish_queue, message_bytes)
