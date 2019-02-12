from big_fiubrother_core.messages import AbstractMessage

class UnknownFaceMessage(AbstractMessage):

    def __init__(self, face_embeddings):
        self.face_embeddings = face_embeddings
