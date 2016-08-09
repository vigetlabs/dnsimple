from .collection import Collection
from .contact    import Contact

class ContactCollection(Collection, object):
    """A collection of Contact objects"""

    def __init__(self, request):
        """
        Parameters
        ----------
        request: Request
            A Request instance to use when fetching API responses
        """
        self.request = request

    def all(self):
        """
        Return a list of all contacts for this account.

        Returns
        -------
        list
            A list of Contact instances
        """
        response = self.request.get('contacts')

        return [
            Contact(self.request, el['contact'])
            for el in response.to_dict(default = [])
        ]

    def find(self, id_or_email):
        """
        Find a specific contact by ID or email address.

        Parameters
        ----------
        id_or_email: int or str
            The ID or email address of the desired contact

        Returns
        -------
        contact: Contact or None
            The matching Contact instance, otherwise ``None``
        """
        contact = None

        try:
            contact = self.__find_by_id(int(id_or_email))
        except ValueError:
            contact = None

        if contact is None:
            contact = self.__find_by_email(str(id_or_email))

        return contact

    def add(self, attributes):
        """
        Create a new contact associated with the current account.

        Parameters
        ----------
        attributes: dict
            Mapping of attribute names to values

        Returns
        -------
        contact: Contact or None
            The new Contact instance, ``None`` on failure
        """
        contact  = None
        response = self.request.post('contacts', {'contact': attributes})

        if response.was_successful():
            contact = Contact(self.request, response.to_dict('contact'))

        return contact

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
