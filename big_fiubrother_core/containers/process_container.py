import multiprocessing
from . import Container, AsyncContainer


class ProcessContainer(AsyncContainer):

    def __init__(self, task, input_interface, output_interface):
        multiprocessing.managers.BaseManager.register('Container', Container)
        self._manager = multiprocessing.managers.BaseManager()
        self._manager.start()

        self._container = self._manager.Container(
            task=task,
            input_interface =input_interface,
            output_interface = output_interface)

        self._process = multiprocessing.Process(target=self._container.run)

    def running(self):
        return self._container.running()

    def start(self):
        self._process.start()

    def stop(self):
        self._container.stop()
        self._manager.shutdown()

    def wait(self):
        self._process.join()
