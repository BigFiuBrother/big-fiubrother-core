import signal


class SignalHandler:

    def __init__(self, stop_callback, message='STOP signal received!'):
        self.stop_callback = stop_callback
        self.message = message

        signal.signal(signal.SIGINT, self.__stop_signal_received)
        signal.signal(signal.SIGTERM, self.__stop_signal_received)

    def __stop_signal_received(self, signum, frame):
        print(self.message)

        self.stop_callback()


