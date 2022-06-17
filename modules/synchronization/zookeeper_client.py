from kazoo.client import KazooClient
from kazoo.exceptions import BadVersionError, NoNodeError 
from contextlib import contextmanager
import logging


class ZookeeperClient:

    def __init__(self, configuration):
        self.host = configuration['host']
        self.port = configuration['port']

        self.client = KazooClient(hosts='{}:{}'.format(self.host, self.port))
        self.client.start()

    def create_node(self, path, data):
        self.client.create(path, data)

    def get_node(self, path):
        data, stat = self.client.get(path)
        return data

    def get_children(self, path):
        return self.client.get_children(path)

    def get_children_count(self, path):
        try:
            return len(self.get_children(path))
        except NoNodeError:
            return -1

    @contextmanager
    def transaction(self):
        transaction = self.client.transaction()

        try:
            yield transaction
        finally:
            results = transaction.commit()

            if "failure" in results:
                logging.error("Zookeeper transaction failed!")

    def delete_node(self, path):
        self.client.delete(path)

    def safe_delete_node(self, path):
        try:
            self.client.delete(path)
            return True
        except BadVersionError as e:
            logging.warn("Bad Version Error")
            return False
        except NoNodeError as e:
            logging.warn("No Node Error")
            return False

    def close(self):
        self.client.stop()
