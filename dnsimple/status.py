from .model import Model

class Status(Model, object):

    def __init__(self, attributes = {}):
        super(Status, self).__init__(None, attributes)
