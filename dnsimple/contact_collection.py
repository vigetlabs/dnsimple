from .collection import Collection
from .contact    import Contact

class ContactCollection(Collection, object):

    def __init__(self, request):
        self.request = request

    def all(self):
        response = self.request.get('contacts')

        return [
            Contact(self.request, el['contact'])
            for el in response.to_dict(default = [])
        ]

    def find(self, id_or_email):
        contact = None

        try:
            contact = self.__find_by_id(int(id_or_email))
        except ValueError:
            contact = None

        if contact is None:
            contact = self.__find_by_email(str(id_or_email))

        return contact

    def add(self, attributes):
        contact  = None
        response = self.request.post('contacts', {'contact': attributes})

        if response.was_successful():
            contact = Contact(self.request, response.to_dict('contact'))

        return contact

    def to_dict(self):
        return [c.to_dict() for c in self.all()]

    def __find_by_id(self, id):
        contact = None

        response = self.request.get('contacts/{0}'.format(id))

        if response.was_successful():
            contact = Contact(self.request, response.to_dict('contact'))

        return contact

    def __find_by_email(self, email):
        contact = None

        matches = [c for c in self.all() if c.email_address == email]

        if len(matches) == 1:
            contact = matches[0]

        return contact
