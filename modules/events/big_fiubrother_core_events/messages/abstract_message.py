class AbstractMessage:

    def type(self):
        return self.__class__.__name__
