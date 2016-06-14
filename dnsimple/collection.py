from .request import Request

class Collection(object):
    def request(self):
        return Request(self.credentials)

    def __iter__(self):
        return iter(self.all())
