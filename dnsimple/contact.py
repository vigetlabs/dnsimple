from .model import Model

class Contact(Model, object):

    def __init__(self, request, data = {}):
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
        self.assign(attributes)

        response = self.request.put(
            'contacts/{0}'.format(self.id),
            {'contact': attributes}
        )

        return response.was_successful()

    def delete(self):
        response = self.request.delete('contacts/{0}'.format(self.id))
        return response.was_successful()
