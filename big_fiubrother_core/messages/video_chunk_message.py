from big_fiubrother_core.messages import AbstractMessage


class VideoChunkMessage(AbstractMessage):

    def __init__(self, camera_id, timestamp, payload):
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.payload = payload

    def id(self):
        return "{}-{}".format(self.camera_id, self.timestamp)
