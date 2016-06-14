from .collection import Collection
from .record     import Record

class RecordCollection(Collection, object):

    def __init__(self, credentials, domain):
        self.credentials = credentials
        self.domain      = domain

    def all(self):
        return map(lambda a: Record(self.credentials, self.domain, a), self.to_dict())

    def find(self, id_or_name):
        record = None

        try:
            record = self.__find_by_id(int(id_or_name))
        except ValueError:
            record = None

        if record is None:
            record = self.__find_by_name(str(id_or_name))

        return record

    def add(self, attributes):
        record   = None
        response = self.request().post('domains/{0}/records'.format(self.domain.name), {'record': attributes})

        if response.was_successful():
            data   = response.to_dict()
            record = Record(self.credentials, self.domain, data.get('record', {}))

        return record

    def to_dict(self):
        response = self.request().get('domains/{0}/records'.format(self.domain.name))

        return map(lambda el: el['record'], response.to_dict())

    def __find_by_id(self, id):
        record   = None
        response = self.request().get('domains/{0}/records/{1}'.format(self.domain.name, id))

        if response.was_successful():
            data   = response.to_dict()
            record = Record(self.credentials, self.domain, data.get('record', {}))

        return record

    def __find_by_name(self, name):
        return next(
            (r for r in self.all() if r.name == name),
            None
        )
