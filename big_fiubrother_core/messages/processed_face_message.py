from big_fiubrother_core.messages import AbstractMessage


class ProcessedFaceMessage(AbstractMessage):

    def __init__(self, frame_id):
        self.frame_id = frame_id
