from big_fiubrother_core.abstract_message import AbstractMessage

class ClusteringMessage(AbstractMessage):

    def __init__(self,face_id, face_embeddings, timestamp):
        self.face_id
        self.face_embeddings = face_embeddings
        self.timestamp = timestamp