from abc import ABC, abstractmethod


class Input:

    @abstractmethod
    def poll(self):
        pass

    def unblock(self):
        pass
