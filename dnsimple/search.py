from .status import Status

class Search:

    def __init__(self, request):
        self.request = request

    def find(self, domain_name):
        response = self.request.get('domains/{0}/check'.format(domain_name))
        return Status(response.to_dict())
