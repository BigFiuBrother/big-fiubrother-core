from big_fiubrother_core.abstract_message import AbstractMessage

class FaceDetectionMessage(AbstractMessage):

    def __init__(self, frame_id, face_id, face):
        self.frame_id = frame_id
        self.face_id = face_id
        self.face = face