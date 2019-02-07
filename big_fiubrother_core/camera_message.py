from big_fiubrother_core.abstract_message import AbstractMessage

class CameraMessage(AbstractMessage):

    def __init__(self, camera_id, frame_bytes, timestamp):
        self.camera_id = camera_id
        self.frame_bytes = frame_bytes
        self.timestamp = timestamp