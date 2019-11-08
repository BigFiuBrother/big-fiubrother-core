from big_fiubrother_core.messages import AbstractMessage


class VideoChunkMessage(AbstractMessage):

    def __init__(self, camera_id, timestamp, payload):
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.payload = payload

    def filename(self):
        return '{}_{}.h264'.format(message.camera_id, message.timestamp)