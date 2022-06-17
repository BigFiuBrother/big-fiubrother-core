# big-fiubrother-core-events

*big-fiubrother-core-events* module centralizes all the necessary components
for an event-driven ecosystem. It offers a client to connect to a message broker 
and produce/consume events. On the other hand, messages are encoded using pickle
module. Currently, the only message broker supported is RabbitMQ.


## Usage

### Producer

```python
from big_fiubrother_core_events.message_clients.rabbitmq.publisher import Publisher
from big_fiubrother_core_events.messages.video_chunk_message import VideoChunkMessage
from big_fiubrother_core_events.messages.marshalling import encode_message

# Configuration for publisher
configuration = {
  'host': 'localhost',
  'username': 'user',
  'password': '1234',
  'exchange': 'fiubrother',
  'routing_key': 'test'
}

# Create a publisher and a message to send
publisher = Publisher(configuration)
message = VideoChunkMessage('camera_id', 'timestamp')

# Encode message
encoded_message = encode_message(message)

# Send message to broker
publisher.publish(encoded_message)
```

### Consumer

```python
from big_fiubrother_core_events.message_clients.rabbitmq.consumer import Consumer


# Print every messaged received
def process_message(message):
    print(message)
    return

# Create a consumer with a callback to handle messages
consumer = Consumer(configuration, process_message)

# Start consuming until the end of times
consumer.start()
```