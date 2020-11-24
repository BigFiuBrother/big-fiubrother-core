from . import S3Client


def video_chunks(configuration):
    return S3Client({**configuration, 'bucket': "video-chunks"})