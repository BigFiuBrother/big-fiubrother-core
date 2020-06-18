from . import Queue
import queue


class MultiThreadQueue(Queue):

    def __init__(self):
        super().__init__(queue.Queue())
