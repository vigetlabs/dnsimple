from .model import Model

class Record(Model, object):

    def __init__(self, request, domain, data = {}):
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
        self.assign(attributes)

        response = self.request.put(
            'domains/{0}/records/{1}'.format(self.domain.name, self.id),
            {'record': attributes}
        )

        return response.was_successful()

    def delete(self):
        response = self.request.delete('domains/{0}/records/{1}'.format(self.domain.name, self.id))
        return response.was_successful()
