from abc import ABC, abstractmethod


class Task(ABC):

    def init(self):
        pass

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    def stop(self):
        pass