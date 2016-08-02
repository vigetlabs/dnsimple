class Collection(object):

    def to_dict(self):
        return [model.to_dict() for model in self.all()]

    def __iter__(self):
        return iter(self.all())
