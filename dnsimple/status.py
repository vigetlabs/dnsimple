from .model import Model

class Status(Model, object):

    def __init__(self, data = {}):
        super(Status, self).__init__(None, data, {
            'available'              : bool,
            'status'                 : str,
            'minimum_number_of_years': int,
            'name'                   : str,
            'price'                  : float,
            'currency'               : str,
            'currency_symbol'        : str
        })
