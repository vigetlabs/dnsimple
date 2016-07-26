from .model             import Model
from .record_collection import RecordCollection

class Domain(Model, object):

    def records(self, name = None, type = None):
        return RecordCollection(self.request, self, name, type)

    def record(self, name, type = None):
        return RecordCollection(self.request, self).find(name, type)

    def delete(self):
        response = self.request.delete('domains/{0}'.format(self.name))
        return response.was_successful()
