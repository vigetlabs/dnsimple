import dnsimple.models

from .exceptions import MultipleResultsException

class Collection(object):

    def to_dict(self):
        """
        Return the dict representation of the collection.

        Returns
        -------
        dict
            Dictionary representation of all instances in the collection
        """
        return [model.to_dict() for model in self.all()]

    def __iter__(self):
        """
        Return an iterator for use in ``for ... in ...`` statements.

        Returns
        -------
        listiterator
            Iterator instance wrapping return value of ``all()``
        """
        return iter(self.all())

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
            dnsimple.models.Contact(self.request, el['contact'])
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
            contact = dnsimple.models.Contact(self.request, response.to_dict('contact'))

        return contact

    def __find_by_id(self, id):
        contact = None

        response = self.request.get('contacts/{0}'.format(id))

        if response.was_successful():
            contact = dnsimple.models.Contact(self.request, response.to_dict('contact'))

        return contact

    def __find_by_email(self, email):
        contact = None

        matches = [c for c in self.all() if c.email_address == email]

        if len(matches) == 1:
            contact = matches[0]

        return contact

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
            dnsimple.models.Domain(self.request, el['domain'])
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
            domain = dnsimple.models.Domain(self.request, response.to_dict('domain', {}))

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
            domain = dnsimple.models.Domain(self.request, response.to_dict('domain', {}))

        return domain

class RecordCollection(Collection, object):
    """A collection of Record objects"""

    def __init__(self, request, domain, name = None, type = None):
        """
        Parameters
        ----------
        request: Request
            A Request instance to use when fetching API responses
        domain: Domain
            A Domain instance to use for fetching records
        name: str or None
            An optional name for filtering records
        type: str or None
            An optional record type for filtering records
        """
        self.request = request
        self.domain  = domain
        self.name    = name
        self.type    = type

    def all(self):
        """
        Return a list of all records for this domain.

        Returns
        -------
        list
            A list of Record instances
        """
        uri      = 'domains/{0}/records'.format(self.domain.name)
        response = self.request.get(uri, self.__filter_params())

        return [
            dnsimple.models.Record(self.request, self.domain, el['record'])
            for el in response.to_dict(default = [])
        ]

    def where(self, name = None, type = None):
        """
        Return a filtered list of records for this domain.

        Parameters
        ----------
        name: str or None
            An optional name for filtering records
        type: str or None
            An optional record type for filtering records

        Returns
        -------
        RecordCollection
        """
        return self.__class__(self.request, self.domain, name, type)

    def find(self, id_or_name, type = None):
        """
        Find a specific record by ID or name, optionally filtering by type.

        Parameters
        ----------
        id_or_name: int or str
            The ID or name of the desired record
        type: str or None
            The type of record (e.g. 'A') to return

        Returns
        -------
        record: Record or None
            The matching Record instance, otherwise ``None``

        Raises
        ------
        MultipleResultsException
            If there is more than 1 record that matches the search criteria
        """
        record = None

        try:
            record = self.__find_by_id(int(id_or_name))
        except ValueError:
            record = None

        if record is None:
            record = self.__find_by_name(str(id_or_name), type)

        return record

    def add(self, attributes):
        """
        Create a new record associated with the current domain.

        Parameters
        ----------
        attributes: dict
            Mapping of attribute names to values

        Returns
        -------
        record: Record or None
            The new Record instance, ``None`` on failure
        """
        record   = None
        response = self.request.post('domains/{0}/records'.format(self.domain.name), {'record': attributes})

        if response.was_successful():
            record = dnsimple.models.Record(self.request, self.domain, response.to_dict('record', {}))

        return record

    def __filter_params(self):
        params = {}

        if self.name is not None:
            params.update({'name': self.name})

        if self.type:
            params.update({'type': self.type})

        return params

    def __find_by_id(self, id):
        record   = None
        response = self.request.get('domains/{0}/records/{1}'.format(self.domain.name, id))

        if response.was_successful():
            record = dnsimple.models.Record(self.request, self.domain, response.to_dict('record', {}))

        return record

    def __find_by_name(self, name, type = None):
        record  = None
        results = self.where(name, type).all()

        if len(results) > 1:
            raise MultipleResultsException("Multiple results returned for query")
        elif len(results) == 1:
            record = results[0]

        return record
