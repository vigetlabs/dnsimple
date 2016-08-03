from .domain import Domain

class Registration:

    def __init__(self, request):
        self.request = request

    def add(self, name, contact):
        domain   = None
        response = self.request.post('domain_registrations', {
            'domain': {'name': name, 'registrant_id': contact.id}
        })

        if response.was_successful():
            domain = Domain(self.request, response.to_dict('domain'))

        return domain
