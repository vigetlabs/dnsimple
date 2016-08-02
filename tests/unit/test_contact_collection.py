from ..context        import dnsimple
from ..request_helper import RequestHelper, request

from dnsimple.contact_collection import ContactCollection
from dnsimple.contact            import Contact

class TestContactCollection(RequestHelper, object):

    def test_all_returns_empty_collection_when_no_records(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', data = [])
        subject = ContactCollection(request)

        contacts = subject.all()

        method.assert_called_once_with('contacts')

        assert contacts == []

    def test_all_returns_all_contacts(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', data = [{'contact': {'id': 1, 'email_address': 'user@host.com'}}])
        subject = ContactCollection(request)

        contacts = subject.all()

        assert len(contacts) == 1

        contact = contacts[0]

        assert isinstance(contact, Contact)
        assert contact.id            == 1
        assert contact.email_address == 'user@host.com'

    def test_find_returns_none_when_neither_id_nor_email_matches(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', success = False)
        subject = ContactCollection(request)

        mocker.patch.object(subject, 'all', lambda: [])

        assert subject.find(1) is None

    def test_find_returns_matching_contact_by_id(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', success = True, data = {'contact': {'id': 1}})
        subject = ContactCollection(request)

        contact = subject.find(1)

        method.assert_called_once_with('contacts/1')

        assert isinstance(contact, Contact)
        assert contact.id == 1

    def test_find_returns_matching_contact_by_name(self, mocker, request):
        contact_1 = Contact(request, {'id': 1, 'email_address': 'user@host.com'})
        contact_2 = Contact(request, {'id': 2, 'email_address': 'other@host.com'})

        method  = self.stub_request(mocker, request, method_name = 'get')
        subject = ContactCollection(request)

        mocker.patch.object(subject, 'all', lambda: [contact_1, contact_2])

        assert subject.find('user@host.com') == contact_1

        method.assert_not_called

    def test_to_dict_returns_empty_array_when_no_records(self, mocker, request):
        subject = ContactCollection(request)

        mocker.patch.object(subject, 'all', lambda: [])

        assert subject.to_dict() == []

    def test_add_creates_new_contact(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'post', success = True, data = {'contact': {'id': 1, 'email_address': 'user@host.com'}})
        subject = ContactCollection(request)

        contact = subject.add({'email_address': 'user@host.com'})

        assert isinstance(contact, Contact)
        assert contact.id            == 1
        assert contact.email_address == 'user@host.com'

        method.assert_called_once_with('contacts', {'contact': {'email_address': 'user@host.com'}})

    def test_add_returns_none_when_adding_fails(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'post', success = False)
        subject = ContactCollection(request)

        assert subject.add({}) is None

    def to_dict_returns_dictionary_representation_of_contacts(self, mocker, request):
        contact_1 = Contact(request, {'id': 1, 'email_address': 'user_1@host.com'})
        contact_2 = Contact(request, {'id': 2, 'email_address': 'user_2@host.com'})

        subject = ContactCollection(request)

        mocker.patch.object(subject, 'all', lambda: [contact_1, contact_2])

        assert subject.to_dict() == [
            {'id': 1, 'email_address': 'user_1@host.com'},
            {'id': 2, 'email_address': 'user_2@host.com'}
        ]

