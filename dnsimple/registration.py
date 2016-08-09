from .domain import Domain

class Registration:
    """Manages domain registrations in DNSimple."""
    def __init__(self, request):
        """
        Parameters
        ----------
        request: Request
            A Request instance to use when fetching API responses
        """
        self.request = request

    def add(self, name, contact):
        """
        Register a new domain name associated with the specified Contact.

        Parameters
        ----------
        name: str
            The name of the domain to register
        contact: Contact
            The contact to associate with the domain registration

        Returns
        -------
        domain: Domain or None
            The newly registered Domain instance, ``None`` on failure
        """
        domain   = None
        response = self.request.post('domain_registrations', {
            'domain': {'name': name, 'registrant_id': contact.id}
        })

        if response.was_successful():
            domain = Domain(self.request, response.to_dict('domain'))

        return domain
