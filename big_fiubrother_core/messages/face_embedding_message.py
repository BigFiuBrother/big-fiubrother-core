from big_fiubrother_core.messages import AbstractMessage


class FaceEmbeddingMessage(AbstractMessage):

    def __init__(self, frame_id, frame_bytes, face_boxes):
        self.frame_id = frame_id
        self.frame_bytes = frame_bytes
        self.face_boxes = face_boxes
