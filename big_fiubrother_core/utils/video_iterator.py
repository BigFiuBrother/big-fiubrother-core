import cv2


class VideoIterator:

    def __init__(self, video_path):
        self.video_path = video_path

    def __iter__(self):
        self.offset = 0
        self.cap = cv2.VideoCapture(self.video_path)
        return self

    def __next__(self):
        ret, frame = self.cap.read()

        if not ret:
            self.cap.release()
            raise StopIteration

        offset = self.offset
        self.offset += 1

        return (offset, frame)
