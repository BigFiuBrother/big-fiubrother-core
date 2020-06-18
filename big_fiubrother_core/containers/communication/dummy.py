from . import Input, Output


class Dummy(Input, Output):

    def poll(self):
        pass

    def push(self):
        pass