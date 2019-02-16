from big_fiubrother_core.messages import AbstractMessage

class UnknownFaceMessage(AbstractMessage):

    def __init__(self, id, face_embeddings):
        self.id = id 
        self.face_embeddings = face_embeddings
