from big_fiubrother_core.messages import AbstractMessage


class AnalyzedVideoChunkMessage(AbstractMessage):

    def __init__(self, video_chunk_id):
        self.video_chunk_id = video_chunk_id

    def id(self):
        return str(self.video_chunk_id)
