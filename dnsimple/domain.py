from .model             import Model
from .record_collection import RecordCollection

class Domain(Model, object):
    def records(self):
        return RecordCollection(self.credentials, self)
