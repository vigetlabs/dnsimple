from . import *

class TestRegistrations:

    def test_domain_registration_availability(self, client):
        status = client.find('google.com')
        assert not status.available
        assert not client.check('google.com')

        status = client.find('this-domain-is-unregistered.com')
        assert status.available
        assert client.check('this-domain-is-unregistered.com')
