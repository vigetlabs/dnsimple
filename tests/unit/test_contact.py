from ..context        import dnsimple
from ..request_helper import RequestHelper, request

from dnsimple.models import Contact

class TestContact(RequestHelper, object):

    def test_assign_assigns_attributes(self, request):
        subject = Contact(request, {'first_name': 'John'})
        subject.assign({'first_name': 'Jane', 'last_name': 'Doe'})

        assert subject.first_name == 'Jane'
        assert subject.last_name  == 'Doe'

    def test_update_sends_update_request(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'put', data = {})
        subject = Contact(request, {'id': 1})

        result = subject.update({'email_address':'user@host.com'})

        method.assert_called_once_with('contacts/1', {'contact': {'email_address':'user@host.com'}})

        assert result is True

    def test_update_returns_false_when_request_fails(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'put', success = False, data = {})
        subject = Contact(request, {'id': 1})

        assert subject.update({}) is False

    def test_update_assigns_attributes(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'put', data = {})
        subject = Contact(request, {'id': 1})

        subject.update({'email_address':'other@host.com'})

        assert subject.email_address == 'other@host.com'

    def test_delete_removes_contact_record(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'delete', data = {})
        subject = Contact(request, {'id': 1})

        result = subject.delete()

        method.assert_called_once_with('contacts/1')

        assert result is True

    def test_delete_returns_false_when_removal_fails(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'delete', success = False)
        subject = Contact(request, {'id': 1})

        assert subject.delete() is False

    def test_to_dict_returns_attributes(self, request):
        subject = Contact(request, {
            "id"               : 1,
            "address1"         : "1 Main Street",
            "address2"         : None,
            "city"             : "Anytown",
            "country"          : "US",
            "email_address"    : "user@host.com",
            "fax"              : None,
            "first_name"       : "First",
            "last_name"        : "Last",
            "job_title"        : None,
            "label"            : None,
            "organization_name": None,
            "phone"            : "+1 303 5551212",
            "postal_code"      : "80301",
            "state_province"   : "CO",
            "created_at"       : "2016-08-01T00:00:00:000Z",
            "updated_at"       : "2016-08-01T00:00:00:000Z",
            "user_id"          : 3
        })

        assert subject.to_dict() == {
            "id"               : 1,
            "address1"         : "1 Main Street",
            "address2"         : None,
            "city"             : "Anytown",
            "country"          : "US",
            "email_address"    : "user@host.com",
            "fax"              : None,
            "first_name"       : "First",
            "last_name"        : "Last",
            "job_title"        : None,
            "label"            : None,
            "organization_name": None,
            "phone"            : "+1 303 5551212",
            "postal_code"      : "80301",
            "state_province"   : "CO",
            "created_at"       : "2016-08-01T00:00:00:000Z",
            "updated_at"       : "2016-08-01T00:00:00:000Z",
            "user_id"          : 3
        }

    def test_not_equal_when_no_ids(self, request):
        a = Contact(request, {})
        b = Contact(request, {})

        assert a != b

    def test_not_equal_when_only_one_id(self, request):
        a = Contact(request, {'id': 1})
        b = Contact(request, {})

        assert a != b

    def test_not_equal_when_ids_differ(self, request):
        a = Contact(request, {'id': 1})
        b = Contact(request, {'id': 2})

        assert a != b

    def test_equal_when_ids_are_the_same(self, request):
        a = Contact(request, {'id': 1})
        b = Contact(request, {'id': 1})

        assert a == b
