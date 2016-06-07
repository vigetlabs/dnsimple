from .collection import Collection
from .record     import Record

class RecordCollection(Collection, object):

    def __init__(self, credentials, domain):
        self.credentials = credentials
        self.domain      = domain

    def all(self):
        return map(lambda a: Record(self.credentials, self.domain, a), self.to_dict())

    def add(self, attributes):
        record   = None
        response = self.request().post('domains/{0}/records'.format(self.domain.name), {'record': attributes})

        if response.was_successful():
            data   = response.to_dict()
            record = Record(self.credentials, self.domain, data['record'])

        return record

    def to_dict(self):
        response = self.request().get('domains/{0}/records'.format(self.domain.name))

        return map(lambda el: el['record'], response.to_dict())
