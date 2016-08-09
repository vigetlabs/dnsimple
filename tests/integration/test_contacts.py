from . import *

class TestContacts:

    def find_contact_by_email(self, client, email):
        contact = None
        matches = [c for c in client.contacts() if c.email_address == email]

        if len(matches) == 1:
            contact = matches[0]

        return contact

    def test_list_contacts(self, client):
        assert client.contacts().all() == []

    def test_create_contacts(self, client):
        contact = client.contacts().add({
            'first_name':     'First',
            'last_name':      'Last',
            'address1':       '1 Main Street',
            'city':           'Anytown',
            'state_province': 'CO',
            'postal_code':    '80301',
            'country':        'US',
            'email_address':  'user@host.com',
            'phone':          '+1 303 5551212'
        })

        assert isinstance(contact, dnsimple.models.Contact)
        assert contact.first_name == 'First'
        assert contact.last_name  == 'Last'

        # Test creation failure
        assert client.contacts().add({}) is None

        assert [c.email_address for c in client.contacts()] == ['user@host.com']

    def test_find_contact(self, client):
        contact = self.find_contact_by_email(client, 'user@host.com')

        assert client.contact('user@host.com') == contact
        assert client.contact(contact.id)      == contact

        assert client.contact('foo@missing.com') is None
        assert client.contact(99999999)          is None

    def test_update_contact(self, client):
        contact = client.contact('user@host.com')

        assert contact.update({'email_address': 'another@host.com'})
        assert contact.email_address == 'another@host.com'

        assert client.contact('user@host.com') is None
        assert client.contact('another@host.com')

        assert contact.update({}) is False

    def test_delete_contacts(self, client):
        count   = len(client.contacts().all())
        contact = self.find_contact_by_email(client, 'another@host.com')

        assert contact.delete() is True
        assert len(client.contacts().all()) == (count - 1)

        # Attempt to delete existing should fail
        assert contact.delete() is False
