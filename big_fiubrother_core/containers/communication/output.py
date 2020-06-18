from abc import ABC, abstractmethod


class Output:

    @abstractmethod
    def send(self, message):
        pass
