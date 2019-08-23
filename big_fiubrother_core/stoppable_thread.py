import threading


class StoppableThread:

    def __init__(self):
        self._thread = threading.Thread(target=self.run)

        self.end_event = threading.Event()
        self.end_event.set()

    def running(self):
        not self.end_event.is_set()

    def start(self):
        self._thread.start()

    def stop(self):
        self.end_event.set()

    def wait(self):
        self._thread.join()

    def run(self):
        try:
            self.end_event.clear()
            
            while not self.end_event.is_set():
                self._execute()
        finally:
            self.end_event.set()

    #Override method in child class
    @abstractmethod
    def _execute(self):
        pass