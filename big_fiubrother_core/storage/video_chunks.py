from . import S3Client


def raw_storage(configuration):
    return S3Client({**configuration, 'bucket': "raw-video-chunks"})

def processed_storage(configuration):
    return S3Client({**configuration, 'bucket': "processed-video-chunks"})