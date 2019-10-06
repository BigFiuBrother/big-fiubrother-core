import pika


class Publisher:

    def __init__(self, configuration):
        self.host = configuration['host']
        self.exchange = configuration['exchange']
        self.routing_key = configuration['routing_key']
        
        self.credentials = pika.PlainCredentials(configuration['username'], configuration['password'])
        self.parameters = pika.ConnectionParameters(host=self.host, credentials=self.credentials)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

    def publish(self, message):
        self.channel.basic_publish(self.exchange, self.routing_key, message.encode())
