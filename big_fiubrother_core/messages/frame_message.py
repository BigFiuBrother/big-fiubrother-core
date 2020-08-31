from big_fiubrother_core.messages import AbstractMessage


class FrameMessage(AbstractMessage):

    def __init__(self, video_chunk_id, frame_id, payload):
        self.video_chunk_id = video_chunk_id
        self.frame_id = frame_id
        self.payload = payload

    def id(self):
        return "{}-{}".format(self.video_chunk_id, self.frame_id)
