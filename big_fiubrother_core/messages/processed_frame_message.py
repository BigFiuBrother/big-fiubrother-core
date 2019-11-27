from big_fiubrother_core.messages import AbstractMessage


class ProcessedFrameMessage(AbstractMessage):

    def __init__(self, video_chunk_id):
        self.video_chunk_id = video_chunk_id
