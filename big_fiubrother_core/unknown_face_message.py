from big_fiubrother_core.abstract_message import AbstractMessage

class UnknownFaceMessage(AbstractMessage):

    def __init__(self, face_embeddings):
        self.face_embeddings = face_embeddings
