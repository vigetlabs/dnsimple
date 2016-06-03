import json

from .request import Request
from .record  import Record

class RecordCollection:

    def __init__(self, domain, credentials):
        self.domain      = domain
        self.credentials = credentials

    def all(self):
        return map(lambda a: Record(self.credentials, self.domain, a), self.to_dict())

    def find(self, id_or_name):
        records = self.all()

        return next(
            (r for r in records if id_or_name in [r.id, r.name]),
            None
        )

    def add(self, attributes):
        request  = Request(self.credentials)
        response = request.post('domains/{0}/records'.format(self.domain.name), {'record': attributes})

        if response.was_successful():
            data   = response.to_dict()
            record = Record(self.credentials, self.domain, data['record'])

        return record

    def to_dict(self):
        request  = Request(self.credentials)
        response = request.get('domains/{0}/records'.format(self.domain.name))

        return map(lambda el: el['record'], response.to_dict())

    def __iter__(self):
        return iter(self.all())
