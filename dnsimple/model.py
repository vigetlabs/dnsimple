class Model(object):
    def __init__(self, request, data = {}, attributes = {}):
        self.request    = request
        self.data       = data
        self.attributes = attributes

    def assign(self, data = {}):
        self.data.update(data)
        return data

    def __getattr__(self, name):
        if self.attributes.has_key(name):
            value = self.data.get(name)

            if value is not None:
                # Cast value based on attribute configuration
                value = self.attributes.get(name, str)(value)

            return value

        raise AttributeError(
            "'{0}' object has no attribute '{1}'".format(self.__class__.__name__, name)
        )

    def to_dict(self):
        return {name: getattr(self, name) for name in self.attributes.keys()}

    def __eq__(self, other):
        return self.id and other.id and self.id == other.id
