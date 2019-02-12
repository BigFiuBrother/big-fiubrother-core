import pickle

class AbstractMessage:

    def encode(self):
        return pickle.dumps(self)

    @staticmethod
    def decode(data):
        return pickle.loads(data)
