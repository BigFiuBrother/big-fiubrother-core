import threading
from abc import ABC, abstractmethod 


class StoppableThread(ABC):

    def __init__(self):
        self._thread = threading.Thread(target=self.run)

        self.end_event = threading.Event()
        self.end_event.set()

    def running(self):
        return not self.end_event.is_set()

    def start(self):
        self._thread.start()

    def stop(self):
        self.end_event.set()
        self._stop()

    def wait(self):
        self._thread.join()

    def run(self):
        try:
            self.end_event.clear()
            self._init()

            while self.running():
                self._execute()
        finally:
            self.end_event.set()

    def _init(self):
        pass

    def _stop(self):
        pass

    @abstractmethod
    def _execute(self):
        pass