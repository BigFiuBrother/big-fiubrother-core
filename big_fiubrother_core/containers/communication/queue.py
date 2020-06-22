from . import Input, Output
import logging


class Queue(Input, Output):

    def __init__(self, queue):
        self._queue = queue

    def poll(self):
        message = self._queue.get()
        
        logging.debug(
            'Received message {}. Queue size: {}'.format(
                str(message),
                self._queue.qsize()))

        return message

    def stop(self):
        self._queue.put(None)

    def send(self, message):
        logging.debug(
            'Sending message {}. Queue size: {}'.format(
                str(message),
                self._queue.qsize()))

        self._queue.put(message)
