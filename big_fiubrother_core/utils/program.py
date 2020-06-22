from . import SignalHandler


class Program:

    def __init__(self, containers):
        self.containers = containers
        self.signal_handler = SignalHandler(stop_callback=self.stop)

    def run(self):
        for container in self.containers:
            container.start()

        for container in self.containers:
            container.wait()

    def stop(self):
        for container in self.containers:
            container.stop()