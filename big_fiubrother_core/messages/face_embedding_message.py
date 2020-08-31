from big_fiubrother_core.messages import AbstractMessage


class FaceEmbeddingMessage(AbstractMessage):

    def __init__(self, video_chunk_id, detected_face_id, face_bytes):
        self.video_chunk_id = video_chunk_id
        self.detected_face_id = detected_face_id
        self.face_bytes = face_bytes

    def id(self):
        return "{}-{}".format(self.video_chunk_id, self.detected_face_id)
