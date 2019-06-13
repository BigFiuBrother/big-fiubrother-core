from big_fiubrother_core.messages import AbstractMessage


class CameraMessage(AbstractMessage):

    def __init__(self, camera_id, frame_bytes, timestamp):

        self.camera_id = camera_id
        self.timestamp = timestamp

        self.frame_bytes = frame_bytes