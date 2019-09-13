import confluent_kafka


class Consumer:

    def __init__(self, configuration):
        self.running = False
        self._consumer = confluent_kafka.Consumer({
            'bootstrap.servers': configuration['servers'],
            'group.id':configuration['group'],
            'auto.offset.reset': configuration['auto_offset_reset']
        })

        self.topics = configuration['topics']


    def start(self):
        self.running = True

        self._consumer.subscribe(self.topics)

        while self.running:
            msg = self._consumer.poll(1.0)

            if msg is not None:
                if msg.error():
                    print("Consumer error: {}".format(msg.error()))
                else:
                    print('Received message: {}'.format(msg.value().decode('utf-8')))
                    self._process_message(msg.value().decode())

    def _process_message(self, message):
        pass

    def stop(self):
        self.running = False
