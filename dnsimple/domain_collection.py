from .collection import Collection
from .domain     import Domain

class DomainCollection(Collection, object):

    def __init__(self, credentials):
        self.credentials = credentials

    def all(self):
        response = self.request().get('domains')

        return [
            Domain(self.credentials, el['domain'])
            for el in response.to_dict(default = [])
        ]

    def find(self, id_or_name):
        domain   = None
        response = self.request().get('domains/{0}'.format(id_or_name))

        if response.was_successful():
            domain = Domain(self.credentials, response.to_dict('domain', {}))

        return domain

    def add(self, attributes):
        domain   = None
        response = self.request().post('domains', {'domain': attributes})

        if response.was_successful():
            domain = Domain(self.credentials, response.to_dict('domain', {}))

        return domain

    def to_dict(self):
        return [d.to_dict() for d in self.all()]
