import threading
import logging


class StoppableThread():

    def __init__(self, task):
        self.task = task
        self.error = None
        self._thread = threading.Thread(target=self.run)

        self.end_event = threading.Event()
        self.end_event.set()

    def running(self):
        return not self.end_event.is_set()

    def start(self):
        self._thread.start()

    def stop(self):
        self.task.stop()

    def wait(self):
        self._thread.join()

    def name(self):
        self.task.name()

    def run(self):
        logging.debug('Task {} started'.format(self.task.name()))
        try:
            self.end_event.clear()
            self.task.init()
            
            self.task.execute()
        except Exception as e:
            logging.error('Task {} raised: {}'.format(self.task.name(), e))
            self.error = e
            raise
        finally:
            logging.debug('Task {} finished'.format(self.task.name()))
            self.end_event.set()
            self.task.close()
