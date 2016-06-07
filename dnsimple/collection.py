from .request import Request

class Collection(object):
    def find(self, id_or_name):
        results = self.all()

        return next(
            (r for r in results if id_or_name in [r.id, r.name]),
            None
        )

    def request(self):
        return Request(self.credentials)

    def __iter__(self):
        return iter(self.all())
