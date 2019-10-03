import pickle


def decode_message(data):
    return pickle.loads(data)

class AbstractMessage:

    def type(self):
        return __class__.__name__

    def encode(self):
        return pickle.dumps(self)