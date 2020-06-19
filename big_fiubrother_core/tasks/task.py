from abc import ABC, abstractmethod


class Task(ABC):

    def name(self):
        return self.__class__.__name__

    @abstractmethod
    def execute(self):
        raise NotImplementedError

    def close(self):
        pass