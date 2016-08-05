from .model             import Model
from .record_collection import RecordCollection

class Domain(Model, object):

    def __init__(self, request, data = {}):
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
        return RecordCollection(self.request, self, name, type)

    def record(self, name, type = None):
        return RecordCollection(self.request, self).find(name, type)

    def delete(self):
        response = self.request.delete('domains/{0}'.format(self.name))
        return response.was_successful()
