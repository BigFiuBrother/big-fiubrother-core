import signal
import logging

class SignalHandler:

    def __init__(self):
        self.stop_signal_received = False
        signal.signal(signal.SIGINT, self.__stop_signal_received)
        signal.signal(signal.SIGTERM, self.__stop_signal_received)

    def __stop_signal_received(self, signum, frame):
        self.stop_signal_received = True
        logging.info('Signal to stop received')