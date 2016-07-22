from .request import Request

class Model(object):
    def __init__(self, credentials, attributes):
        self.credentials = credentials
        self.attributes  = self.assign(attributes)

    def to_dict(self):
        return self.attributes

    def request(self):
        return Request(self.credentials)

    def assign(self, attributes):
        for (key, value) in attributes.items():
            setattr(self, key, value)

        return attributes