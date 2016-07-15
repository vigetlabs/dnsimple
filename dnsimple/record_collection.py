from .collection import Collection
from .record     import Record

class MultipleResultsException(Exception):
    pass

class RecordCollection(Collection, object):

    def __init__(self, credentials, domain, name = None, type = None):
        self.credentials = credentials
        self.domain      = domain
        self.name        = name
        self.type        = type

    def all(self):
        uri      = 'domains/{0}/records'.format(self.domain.name)
        response = self.request().get(uri, self.__filter_params())

        return [
            Record(self.credentials, self.domain, el['record'])
            for el in response.to_dict(default = [])
        ]

    def where(self, name = None, type = None):
        return self.__class__(self.credentials, self.domain, name, type)

    def find(self, id_or_name, type = None):
        record = None

        try:
            record = self.__find_by_id(int(id_or_name))
        except ValueError:
            record = None

        if record is None:
            record = self.__find_by_name(str(id_or_name), type)

        return record

    def add(self, attributes):
        record   = None
        response = self.request().post('domains/{0}/records'.format(self.domain.name), {'record': attributes})

        if response.was_successful():
            record = Record(self.credentials, self.domain, response.to_dict('record', {}))

        return record

    def to_dict(self):
        return [r.to_dict() for r in self.all()]

    def __filter_params(self):
        params = {}

        if self.name is not None:
            params.update({'name': self.name})

        if self.type:
            params.update({'type': self.type})

        return params

    def __find_by_id(self, id):
        record   = None
        response = self.request().get('domains/{0}/records/{1}'.format(self.domain.name, id))

        if response.was_successful():
            record = Record(self.credentials, self.domain, response.to_dict('record', {}))

        return record

    def __find_by_name(self, name, type = None):
        record  = None
        results = self.where(name, type).all()

        if len(results) > 1:
            raise MultipleResultsException("Multiple results returned for query")
        elif len(results) == 1:
            record = results[0]

        return record
