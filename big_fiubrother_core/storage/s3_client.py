import logging
from math import trunc
from time import time
from minio import Minio
from minio.error import ResponseError
from contextlib import contextmanager


class S3Client:

    FETCH = "FETCH"
    UPLOAD = "UPLOAD"

    def __init__(self, configuration):
        self._host = configuration['host']
        self._port = configuration['port']
        self._access_key = configuration['access_key']
        self._secret_key = configuration['secret_key']
        self.bucket = configuration['bucket']

        self.client = Minio("{}:{}".format(self._host, self._port),
            access_key=self._access_key,
            secret_key=self._secret_key,
            secure=False)

    def store(self, id, data, size):
        with self.timer(id, self.UPLOAD):
            try:
                self.client.put_object(self.bucket, str(id), data=data, length=size)
            except ResponseError as err:
                logging.exception("Store failed for {}".format(id))
                raise

    def store_file(self, id, filepath):
        with self.timer(id, self.UPLOAD):
            try:
                self.client.fput_object(self.bucket, str(id), filepath)
            except ResponseError as err:
                logging.exception("Store file failed for {} -> {}".format(id, filepath))
                raise

    def retrieve(self, id):
        with self.timer(id, self.UPLOAD):
            try:
                return self.client.get_object(self.bucket, str(id)).data
            except ResponseError as err:
                logging.exception("Retrieve failed for {}".format(id))
                raise

    def retrieve_file(self, id, filepath):
        with self.timer(id, self.UPLOAD):
            try:
                self.client.fget_object(self.bucket, str(id), filepath)
            except ResponseError as err:
                logging.exception("Retrieve file failed for {} -> {}".format(id, filepath))
                raise

    @contextmanager
    def timer(self,id, operation):
        start = time()
        yield
        end = time()
        logging.info("S3 {} - {} for {} time elapsed: {}".format(
            self.bucket,
            operation, 
            id,
            trunc((end - start) * 1000)))