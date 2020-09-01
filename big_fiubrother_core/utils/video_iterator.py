class VideoIterator:

    def __init__(self, video_capture):
        self.video_capture = video_capture
        self.offset = 0

    def __iter__(self):
        return self

    def __next__(self):
        ret, frame = self.video_capture.read()

        if not ret:
            self.video_capture.release()
            raise StopIteration

        offset = self.offset
        self.offset += 1

        return (offset, frame)
