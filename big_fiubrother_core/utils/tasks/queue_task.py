from . import Task
from abc import abstractmethod


class QueueTask(Task):

    def __init__(self, input_queue):
        self.input_queue = input_queue
        self.running = False

    def execute(self):
        self.running = True

        while self.running:
            message = self.input_queue.get()

            if message is not None:
                self.execute_with(message)
                
    @abstractmethod
    def execute_with(self, message):
        raise NotImplementedError

    def stop(self):
        self.running = False
        self.input_queue.put(None)
