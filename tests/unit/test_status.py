from ..context import dnsimple

from dnsimple.models import Status

class TestStatus:
    def test_assign_assigns_attributes(self):
        subject = Status()
        subject.assign({'available':False})

        assert subject.available == False

    def test_price_returns_float(self ):
        subject = Status({'price': '14.50'})
        assert subject.price == 14.5

    def test_to_dict_returns_mapped_attributes(self):
        subject = Status({
            "available"              : False,
            "currency"               : "USD",
            "currency_symbol"        : "$",
            "minimum_number_of_years": 1,
            "name"                   : "google.com",
            "price"                  : "14.0",
            "status"                 : "unavailable"
        })

        assert subject.to_dict() == {
            "available"              : False,
            "currency"               : "USD",
            "currency_symbol"        : "$",
            "minimum_number_of_years": 1,
            "name"                   : "google.com",
            "price"                  : 14.0,
            "status"                 : "unavailable"
        }