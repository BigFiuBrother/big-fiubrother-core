from abc import ABC, abstractmethod


class AsyncContainer:

    @abstractmethod
    def running(self):
        pass

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def wait(self):
        pass
