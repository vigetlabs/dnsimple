from .collection import Collection
from .domain     import Domain

class DomainCollection(Collection, object):

    def __init__(self, credentials):
        self.credentials = credentials

    def all(self):
        return map(lambda a: Domain(self.credentials, a), self.to_dict())

    def add(self, attributes):
        domain   = None
        response = self.request().post('domains', {'domain': attributes})

        if response.was_successful():
            data   = response.to_dict()
            domain = Domain(self.credentials, data['domain'])

        return domain

    def to_dict(self):
        response = self.request().get('domains')
        return map(lambda el: el['domain'], response.to_dict())
