import signal


class SignalHandler:

    def __init__(self, callback=None, processes=[], message='STOP signal received!'):
        self.stop_signal_received = False
        self.callback = callback
        self.processes = processes
        self.message = message

        signal.signal(signal.SIGINT, self.__stop_signal_received)
        signal.signal(signal.SIGTERM, self.__stop_signal_received)

    def __stop_signal_received(self, signum, frame):
        self.stop_signal_received = True
        
        print(self.message)

        for process in processes:
            process.stop()

        if self.callback is not None:
            self.callback()


