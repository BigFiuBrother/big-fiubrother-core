from big_fiubrother_core.messages import AbstractMessage


class FaceClassificationMessage(AbstractMessage):

    def __init__(self, camera_id, timestamp, frame_id, frame_bytes, face_boxes, face_embeddings):

        self.camera_id = camera_id
        self.timestamp = timestamp

        self.frame_id = frame_id
        self.frame_bytes = frame_bytes

        self.face_boxes = face_boxes
        self.face_embeddings = face_embeddings
