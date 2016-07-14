from .request import Request

class Model(object):
    def __init__(self, credentials, attributes):
        self.credentials = credentials
        self.attributes  = attributes

        for (key, value) in self.attributes.items():
            setattr(self, key, value)

    def to_dict(self):
        return self.attributes

    def request(self):
        return Request(self.credentials)
