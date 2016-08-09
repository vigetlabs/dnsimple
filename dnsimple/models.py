from .collections import RecordCollection

class Model(object):
    def __init__(self, request, data = {}, attributes = {}):
        self.request    = request
        self.data       = data
        self.attributes = attributes

    def assign(self, data = {}):
        """
        Assign attributes to the current model instance.

        Parameters
        ----------
        data: dict
            Mapping of attribute names to values

        Returns
        -------
        dict
            Key / value pairs passed to method
        """
        self.data.update(data)
        return data

    def to_dict(self):
        """
        Return the dictionary representation of the model instance.

        Returns
        -------
        dict
            Key / value pairs representing all attributes
        """
        return {name: getattr(self, name) for name in self.attributes.keys()}

    def __getattr__(self, name):
        if self.attributes.has_key(name):
            value = self.data.get(name)

            if value is not None:
                # Cast value based on attribute configuration
                value = self.attributes.get(name, str)(value)

            return value

        raise AttributeError(
            "'{0}' object has no attribute '{1}'".format(self.__class__.__name__, name)
        )

    def __eq__(self, other):
        return self.id and other.id and self.id == other.id

class Contact(Model, object):
    """
    A representation of a contact resource in DNSimple.

    Properties
    ----------
    id               : int
    label            : str
    first_name       : str
    last_name        : str
    email_address    : str
    organization_name: str
    job_title        : str
    address1         : str
    address2         : str
    city             : str
    state_province   : str
    country          : str
    postal_code      : str
    phone            : str
    fax              : str
    user_id          : int
    created_at       : str
    updated_at       : str
    """
    def __init__(self, request, data = {}):
        """
        Initialize a Contact resource.

        Parameters
        ----------
        request: Request
            A Request instance to use when fetching API responses
        data: dict
            Mapping of attribute names to values
        """
        super(Contact, self).__init__(request, data, {
            'id'               : int,
            'state_province'   : str,
            'city'             : str,
            'first_name'       : str,
            'last_name'        : str,
            'user_id'          : int,
            'updated_at'       : str,
            'address1'         : str,
            'address2'         : str,
            'fax'              : str,
            'label'            : str,
            'organization_name': str,
            'phone'            : str,
            'postal_code'      : str,
            'country'          : str,
            'created_at'       : str,
            'email_address'    : str,
            'job_title'        : str
        })

    def update(self, attributes):
        """
        Update an existing contact.

        Parameters
        ----------
        attributes: dict

        Returns
        -------
        bool
            Was the update successful?
        """
        self.assign(attributes)

        response = self.request.put(
            'contacts/{0}'.format(self.id),
            {'contact': attributes}
        )

        return response.was_successful()

    def delete(self):
        """
        Delete an existing contact.

        Returns
        -------
        bool
            Was deletion successful?
        """
        response = self.request.delete('contacts/{0}'.format(self.id))
        return response.was_successful()

class Domain(Model, object):
    """
    A representation of a domain resource in DNSimple.

    Properties
    ----------
    id             : int
    record_count   : int
    user_id        : int
    name           : str
    unicode_name   : str
    expires_on     : str
    state          : str
    whois_protected: bool
    token          : str
    service_count  : int
    lockable       : bool
    auto_renew     : bool
    account_id     : int
    registrant_id  : int
    created_at     : str
    updated_at     : str
    """
    def __init__(self, request, data = {}):
        """
        Initialize a Domain resource.

        Parameters
        ----------
        request: Request
            A Request instance to use when fetching API responses
        data: dict
            Mapping of attribute names to values
        """
        super(Domain, self).__init__(request, data, {
            'id'             : int,
            'record_count'   : int,
            'user_id'        : int,
            'name'           : str,
            'created_at'     : str,
            'state'          : str,
            'updated_at'     : str,
            'whois_protected': bool,
            'token'          : str,
            'service_count'  : int,
            'lockable'       : bool,
            'auto_renew'     : bool,
            'unicode_name'   : str,
            'registrant_id'  : int,
            'expires_on'     : str,
            'account_id'     : int
        })

    def records(self, name = None, type = None):
        """
        Fetch a list of records associated with this domain.

        Parameters
        ----------
        name: str or None
            Find records with this name if provided
        type: str or None
            Find records of this type (e.g. 'A') if provided

        Returns
        -------
        RecordCollection
        """
        return RecordCollection(self.request, self, name, type)

    def record(self, name, type = None):
        """
        Find a specific record by name associated with this domain.

        Parameters
        ----------
        name: str
            The name of the record to find, can be the empty string ('')
        type: str or None
            The type of record to find (e.g. 'A')

        Returns
        -------
        record: Record or None
            Matching record or None if not found

        Raises
        ------
        MultipleResultsException
            If multiple records match the search criteria
        """
        return RecordCollection(self.request, self).find(name, type)

    def delete(self):
        """
        Delete an existing domain.

        Returns
        -------
        bool
            Was deletion successful?
        """
        response = self.request.delete('domains/{0}'.format(self.name))
        return response.was_successful()

class Record(Model, object):
    """
    A representation of a DNS record resource in DNSimple.

    Properties
    ----------
    id           : int
    name         : str
    record_type  : str
    content      : str
    ttl          : int
    prio         : int
    system_record: bool
    domain_id    : int
    parent_id    : int
    created_at   : str
    updated_at   : str
    """
    def __init__(self, request, domain, data = {}):
        """
        Initialize a Record resource.

        Parameters
        ----------
        request: Request
            A Request instance to use when fetching API responses
        domain: Domain
            A Domain instance that this record belongs to
        data: dict
            Mapping of attribute names to values
        """
        self.domain = domain

        super(Record, self).__init__(request, data, {
            'id'           : int,
            'name'         : str,
            'prio'         : int,
            'record_type'  : str,
            'system_record': bool,
            'created_at'   : str,
            'updated_at'   : str,
            'domain_id'    : int,
            'content'      : str,
            'parent_id'    : int,
            'ttl'          : int
        })

    def update(self, attributes):
        """
        Update an existing record.

        Parameters
        ----------
        attributes: dict

        Returns
        -------
        bool
            Was the update successful?
        """
        self.assign(attributes)

        response = self.request.put(
            'domains/{0}/records/{1}'.format(self.domain.name, self.id),
            {'record': attributes}
        )

        return response.was_successful()

    def delete(self):
        """
        Delete an existing record.

        Returns
        -------
        bool
            Was deletion successful?
        """
        response = self.request.delete('domains/{0}/records/{1}'.format(self.domain.name, self.id))
        return response.was_successful()

class Status(Model, object):
    """
    A representation of a domain registration status in DNSimple.

    Properties
    ----------
    name                   : str
    available              : bool
    status                 : str
    minimum_number_of_years: int
    price                  : float
    currency               : str
    currency_symbol        : str
    """
    def __init__(self, data = {}):
        """
        Initialize a Status resource.

        Parameters
        ----------
        data: dict
            Mapping of attribute names to values
        """
        super(Status, self).__init__(None, data, {
            'available'              : bool,
            'status'                 : str,
            'minimum_number_of_years': int,
            'name'                   : str,
            'price'                  : float,
            'currency'               : str,
            'currency_symbol'        : str
        })
