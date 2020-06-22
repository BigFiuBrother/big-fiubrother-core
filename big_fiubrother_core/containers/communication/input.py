from abc import ABC, abstractmethod


class Input(ABC):

    @abstractmethod
    def poll(self):
        pass

    @abstractmethod
    def stop(self):
        pass
