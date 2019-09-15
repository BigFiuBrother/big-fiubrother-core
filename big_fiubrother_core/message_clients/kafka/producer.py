import confluent_kafka


class Producer:

    def __init__(self, configuration):
        self._producer = confluent_kafka.Producer({'bootstrap.servers': configuration['servers']})  
        self.topic = configuration['topic']

    def _delivery_report(self, err, msg):
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

    def produce(self, message):
        self._producer.produce(self.topic, message.encode(), callback= self._delivery_report)
        self._producer.poll(0)

    def flush(self):
        self._producer.flush()