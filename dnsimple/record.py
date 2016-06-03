from .request import Request

class Record:

    def __init__(self, credentials, domain, attributes):
        self.credentials = credentials
        self.domain      = domain
        self.attributes  = attributes

        for (key, value) in self.attributes.items():
            setattr(self, key, value)

    def delete(self):
        request  = Request(self.credentials)
        response = request.delete('domains/{0}/records/{1}'.format(self.domain.name, self.id))

        return response.was_successful()

    def to_dict(self):
        return self.attributes
