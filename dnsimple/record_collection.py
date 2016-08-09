from .collection import Collection
from .record     import Record

class MultipleResultsException(Exception):
    pass

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
            Record(self.request, self.domain, el['record'])
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
            record = Record(self.request, self.domain, response.to_dict('record', {}))

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
            record = Record(self.request, self.domain, response.to_dict('record', {}))

        return record

    def __find_by_name(self, name, type = None):
        record  = None
        results = self.where(name, type).all()

        if len(results) > 1:
            raise MultipleResultsException("Multiple results returned for query")
        elif len(results) == 1:
            record = results[0]

        return record
