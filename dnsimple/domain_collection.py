from .collection import Collection
from .domain     import Domain

class DomainCollection(Collection, object):
    """A collection of Domain objects"""

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
        Return a list of all domains for this account.

        Returns
        -------
        list
            A list of Domain instances
        """
        response = self.request.get('domains')

        return [
            Domain(self.request, el['domain'])
            for el in response.to_dict(default = [])
        ]

    def find(self, id_or_name):
        """
        Find a specific domain by ID or name.

        Parameters
        ----------
        id_or_name: int or str
            The ID or name of the desired domain

        Returns
        -------
        domain: Domain or None
            The matching Domain instance, otherwise ``None``
        """
        domain   = None
        response = self.request.get('domains/{0}'.format(id_or_name))

        if response.was_successful():
            domain = Domain(self.request, response.to_dict('domain', {}))

        return domain

    def add(self, attributes):
        """
        Create a new domain associated with the current account.

        Parameters
        ----------
        attributes: dict
            Mapping of attribute names to values

        Returns
        -------
        domain: Domain or None
            The new Domain instance, ``None`` on failure
        """
        domain   = None
        response = self.request.post('domains', {'domain': attributes})

        if response.was_successful():
            domain = Domain(self.request, response.to_dict('domain', {}))

        return domain
