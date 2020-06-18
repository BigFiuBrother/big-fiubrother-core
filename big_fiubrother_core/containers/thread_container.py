import threading
from . import Container, AsyncContainer
from .communication import Dummy


class ThreadContainer(AsyncContainer):

    def __init__(self, task, input_interface=Dummy(), output_interface=Dummy()):
        self._container = Container(
            task=task,
            input_interface =input_interface,
            output_interface = output_interface)

        self._thread = threading.Thread(target=self._container.run)

    def running(self):
        return self._container.running()

    def start(self):
        self._thread.start()

    def stop(self):
        self._container.stop()

    def wait(self):
        self._thread.join()
