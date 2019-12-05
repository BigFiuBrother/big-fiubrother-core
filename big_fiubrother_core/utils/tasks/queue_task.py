from . import Task
from abc import abstractmethod
from uuid import uuid4 as uuid
import logging


class QueueTask(Task):

    def __init__(self, input_queue):
        self.input_queue = input_queue
        self.running = False

    def execute(self):
        self.running = True

        while self.running:
            message = self.input_queue.get()
            message_id = uuid()
            logging.debug(
                'Received message {}. Queue size: {}'.format(
                    str(message_id),
                    self.input_queue.qsize()))

            if message is not None:
                self.execute_with(message)

                logging.debug(
                    'Executed message {}. Queue size: {}'.format(
                        str(message_id),
                        self.input_queue.qsize()))

    @abstractmethod
    def execute_with(self, message):
        raise NotImplementedError

    def stop(self):
        self.running = False
        self.input_queue.put(None)
