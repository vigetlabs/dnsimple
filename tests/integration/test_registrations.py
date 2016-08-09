import pytest

from . import *

def find_or_create_contact(client, email):
    contact = client.contact(email)

    if not contact:
        contact = client.contacts().add({
            'first_name':     'First',
            'last_name':      'Last',
            'address1':       '1 Main Street',
            'city':           'Anytown',
            'state_province': 'CO',
            'postal_code':    '80301',
            'country':        'US',
            'email_address':  email,
            'phone':          '+1 303 5551212'
        })

    return contact

@pytest.fixture
def contact(client):
    return find_or_create_contact(client, 'user@host.com')

class TestRegistrations:

    def test_domain_registration_availability(self, client):
        status = client.find('google.com')
        assert not status.available
        assert not client.check('google.com')

        status = client.find(unregistered_domain_name)
        assert status.available
        assert client.check(unregistered_domain_name)

    def test_registering_domain(self, client, contact):
        domain = client.register(unregistered_domain_name, contact)

        assert isinstance(domain, dnsimple.models.Domain)
        assert domain.name == unregistered_domain_name

        status = client.find(unregistered_domain_name)
        assert not status.available
        assert not client.check(unregistered_domain_name)

        domain = client.register('google.com', contact)
        assert domain is None

    def test_transferring_domain(self, client, contact):
        registered_domain_name = unregistered_domain_name # This was registered in previous test

        target_contact = find_or_create_contact(client, 'other@host.com')

        # Transferring within the account will fail, but this at least exercises the API code
        assert not client.transfer(registered_domain_name, target_contact)
