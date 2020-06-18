import logging
from minio import Minio
from minio.error import ResponseError

class S3Storage:

    def __init__(self, configuration):
        self.host = configuration['host']
        self.access_key = configuration['access_key']
        self.secret_key = configuration['secret_key']
        self.bucket = configuration['bucket']

        self.client = Minio(self.host, 
            access_key=self.access_key,
            secret_key=self.secret_key,
            secure=False)

    def store(self, id, object, size):
        try:
            self.client.put_object(self.bucket, id, data=object, length=size)
        except ResponseError as err:
            logging.exception("Store failed for {} -> {}".format(id, filepath))
            raise       

    def store_file(self, id, filepath):
        try:
            self.client.fput_object(self.bucket, id, filepath)
        except ResponseError as err:
            logging.exception("Store file failed for {} -> {}".format(id, filepath))
            raise

    def retrieve(self, id, filepath)
        try:
            return minioClient.get_object(self.bucket, id, filepath).data
        except ResponseError as err:
            logging.exception("Retrieve failed for {} -> {}".format(id, filepath))
            raise

    def retrieve_file(self, id, filepath)
        try:
            minioClient.fget_object(self.bucket, id, filepath)
        except ResponseError as err:
            logging.exception("Retrieve file failed for {} -> {}".format(id, filepath))
            raise
