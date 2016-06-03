from .domain  import Domain
from .request import Request

class DomainCollection:

    def __init__(self, credentials):
        self.credentials = credentials

    def all(self):
        return map(lambda a: Domain(self.credentials, a), self.to_dict())

    def find(self, id_or_name):
        domains = self.all()

        return next(
            (d for d in domains if id_or_name in [d.id, d.name]),
            None
        )

    def add(self, attributes):
        domain = None

        request  = Request(self.credentials)
        response = request.post('domains', {'domain': attributes})

        if response.was_successful():
            data   = response.to_dict()
            domain = Domain(self.credentials, data['domain'])

        return domain

    def to_dict(self):
        request  = Request(self.credentials)
        response = request.get('domains')

        return map(lambda el: el['domain'], response.to_dict())

    def __iter__(self):
        return iter(self.all())
