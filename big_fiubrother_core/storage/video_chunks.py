from . import S3Client


def raw_storage(configuration):
    return S3Client({**configuration, 'bucket': "raw_video_chunks"})

def processed_storage(configuration):
    return S3Client({**configuration, 'bucket': "processed_video_chunks"})