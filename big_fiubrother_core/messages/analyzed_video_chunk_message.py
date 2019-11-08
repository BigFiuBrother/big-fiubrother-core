from big_fiubrother_core.messages import AbstractMessage


class AnalyzedVideoChunkMessage(AbstractMessage):

    def __init__(self, video_chunk_id, frame_ids):
        self.video_chunk_id = video_chunk_id
        self.frame_ids = frame_ids