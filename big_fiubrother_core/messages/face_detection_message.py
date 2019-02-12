from big_fiubrother_core.messages import AbstractMessage

class FaceDetectionMessage(AbstractMessage):

    def __init__(self, frame_id, face_id, face):
        self.frame_id = frame_id
        self.face_id = face_id
        self.face = face