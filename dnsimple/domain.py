from .record_collection import RecordCollection

class Domain:
    def __init__(self, credentials, attributes):
        self.credentials = credentials
        self.attributes  = attributes

        for (key, value) in self.attributes.items():
            setattr(self, key, value)

    def records(self):
        return RecordCollection(self.credentials, self)

    def to_dict(self):
        return self.attributes
