from .model import Model

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
