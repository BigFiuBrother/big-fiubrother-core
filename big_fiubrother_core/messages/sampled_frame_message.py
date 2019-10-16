from big_fiubrother_core.messages import AbstractMessage


class SampledFrameMessage(AbstractMessage):

    def __init__(self, chunk_id, offset, frame):
        self.chunk_id = chunk_id
        self.offset = offset
        self.frame = frame
