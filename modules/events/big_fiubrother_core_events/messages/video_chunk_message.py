class VideoChunkMessage:

    def __init__(self, camera_id, timestamp):
        self.camera_id = camera_id
        self.timestamp = timestamp

    def id(self):
        return f"{self.camera_id}-{self.timestamp}"
