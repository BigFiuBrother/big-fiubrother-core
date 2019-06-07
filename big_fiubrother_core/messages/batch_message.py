from big_fiubrother_core.messages import AbstractMessage


class BatchMessage(AbstractMessage):

    def __init__(self, messages):
        self.messages = messages
