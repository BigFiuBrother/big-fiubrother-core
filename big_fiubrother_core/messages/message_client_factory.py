from big_fiubrother_core.messages.rabbitmq import *

class MessageClientFactory:

    @staticmethod
    def buildPublisher(settings):

        client_type = settings['type']
        if client_type == "queue_publisher_rabbitmq":
            host = settings['rabbitmqhost']
            queue_name = settings['queue_name']
            return QueuePublisherRabbitMq(host, queue_name)

    @staticmethod
    def buildConsumer(settings, consume_callback):

        client_type = settings['type']
        if client_type == "queue_consumer_rabbitmq":
            host = settings['rabbitmqhost']
            queue_name = settings['queue_name']
            return QueueConsumerRabbitMq(host, queue_name, consume_callback)