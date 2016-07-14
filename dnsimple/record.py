from .model   import Model

class Record(Model, object):

    def __init__(self, credentials, domain, attributes):
        self.domain = domain

        super(Record, self).__init__(credentials, attributes)

    def delete(self):
        response = self.request().delete('domains/{0}/records/{1}'.format(self.domain.name, self.id))
        return response.was_successful()
