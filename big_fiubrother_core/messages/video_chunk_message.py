from big_fiubrother_core.messages import AbstractMessage


class VideoChunkMessage(AbstractMessage):

    def __init__(self, camera_id, video_chunk, timestamp):
        self.camera_id = camera_id
        self.timestamp = timestamp
        self.video_chunk = video_chunk