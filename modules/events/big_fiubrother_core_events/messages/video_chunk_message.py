from .abstract_message import AbstractMessage


class VideoChunkMessage(AbstractMessage):

    def __init__(self, camera_id, timestamp):
        self.camera_id = camera_id
        self.timestamp = timestamp

    def id(self):
        return "{}-{}".format(self.camera_id, self.timestamp)
