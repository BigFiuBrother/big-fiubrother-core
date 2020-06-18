import pickle


def decode_message(data):
    return pickle.loads(data)

def encode_message(encoded_data):
    return pikcle.dumps(encoded_data)

class AbstractMessage:

    def type(self):
        return self.__class__.__name__
