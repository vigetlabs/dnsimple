from .model import Model

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
