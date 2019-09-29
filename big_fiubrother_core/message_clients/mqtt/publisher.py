import paho.mqtt.client as mqtt
import uuid


class Publisher:

    def __init__(self, settings):
        self.host = settings['connection_url']
        self.topic = settings['topic']
        self.qos = settings['qos']

        self.client = mqtt.Client(client_id=uuid.uuid1().hex,
                                  clean_session=True)

        self.client.username_pw_set(settings['user'], settings['password'])
        self.client.connect(self.host)
        self.client.loop_start()
    
    def send(self, message):
        result = self.client.publish(topic=self.topic,
                                     payload=message,
                                     qos=self.qos)

    def close(self):
        self.client.loop_stop()
        self.client.disconnect()
