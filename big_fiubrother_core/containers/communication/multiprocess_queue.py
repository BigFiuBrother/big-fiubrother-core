from . import Queue
import multiprocessing
import logging


class MultiProcessQueue(Queue):

    def __init__(self):
        super().__init__(multiprocessing.Queue())
