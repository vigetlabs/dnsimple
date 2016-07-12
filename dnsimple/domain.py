from .model             import Model
from .record_collection import RecordCollection

class Domain(Model, object):

    def records(self, name = None, type = None):
        return RecordCollection(self.credentials, self, name, type)

    def record(self, name, type = None):
        return RecordCollection(self.credentials, self).find(name, type)
