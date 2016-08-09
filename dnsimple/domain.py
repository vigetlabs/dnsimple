from .model             import Model
from .record_collection import RecordCollection

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
