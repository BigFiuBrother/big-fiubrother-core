from big_fiubrother_core.messages import AbstractMessage


class VideoChunkMessage(AbstractMessage):

    def __init__(self, camera_id, timestamp, payload):
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.payload = payload

    def __str__(self):
        if self._str is None:
            self._str = "{}_{}".format(self.camera_id, self.timestamp)

        return self._str
