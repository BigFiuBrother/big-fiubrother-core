from big_fiubrother_core.messages import AbstractMessage


class FaceClassificationMessage(AbstractMessage):

    def __init__(self, video_chunk_id, face_id, face_embedding):
        self.video_chunk_id = video_chunk_id
        self.face_id = face_id
        self.face_embedding = face_embedding

    def id(self):
        return "{}-{}".format(self.video_chunk_id, self.face_id)