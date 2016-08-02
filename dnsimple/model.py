class Model(object):
    def __init__(self, request, attributes):
        self.request    = request
        self.attributes = self.assign(attributes)

    def id(self):
        value = None

        try:
            value = getattr(self, 'id')
        except AttributeError:
            pass

        return value

    def to_dict(self):
        return self.attributes

    def assign(self, attributes):
        for (key, value) in attributes.items():
            setattr(self, key, value)

        return attributes

    def __eq__(self, other):
        return self.id and other.id and self.id == other.id
