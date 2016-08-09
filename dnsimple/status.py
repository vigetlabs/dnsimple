from .model import Model

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
