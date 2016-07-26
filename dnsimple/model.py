class Model(object):
    def __init__(self, request, attributes):
        self.request    = request
        self.attributes = self.assign(attributes)

    def to_dict(self):
        return self.attributes

    def assign(self, attributes):
        for (key, value) in attributes.items():
            setattr(self, key, value)

        return attributes