import pytest

from ..context         import dnsimple
from ..request_helper  import RequestHelper, request

from dnsimple.domain            import Domain
from dnsimple.record_collection import RecordCollection

@pytest.fixture
def subject(request):
    return Domain(request, {'id': 1, 'name':'example.com'})

class TestDomain(RequestHelper, object):

    def setup_method(self, method):
        self.original_find = dnsimple.record_collection.RecordCollection.find

    def teardown_method(self, method):
        dnsimple.record_collection.RecordCollection.find = self.original_find

    def test_assign_assigns_attributes(self, subject):
        subject.assign({'name': 'foo.com'})

        assert subject.id   == 1
        assert subject.name == 'foo.com'

    def test_to_dict_returns_attributes(self, request):
        subject = Domain(request, {
            "id"             : 1,
            "account_id"     : 2,
            "auto_renew"     : False,
            "created_at"     : "2016-08-01T00:00:00:000Z",
            "expires_on"     : None,
            "lockable"       : True,
            "name"           : "foo.com",
            "record_count"   : 5,
            "registrant_id"  : 300,
            "service_count"  : 0,
            "state"          : "hosted",
            "token"          : "token",
            "unicode_name"   : "example.com",
            "updated_at"     : "2016-08-01T00:00:00:000Z",
            "user_id"        : 400,
            "whois_protected": False
        })

        assert subject.to_dict() == {
            "id"             : 1,
            "account_id"     : 2,
            "auto_renew"     : False,
            "created_at"     : "2016-08-01T00:00:00:000Z",
            "expires_on"     : None,
            "lockable"       : True,
            "name"           : "foo.com",
            "record_count"   : 5,
            "registrant_id"  : 300,
            "service_count"  : 0,
            "state"          : "hosted",
            "token"          : "token",
            "unicode_name"   : "example.com",
            "updated_at"     : "2016-08-01T00:00:00:000Z",
            "user_id"        : 400,
            "whois_protected": False
        }

    def test_records_creates_instance_of_collection(self,  request, subject):
        collection = subject.records()

        assert isinstance(collection, RecordCollection)

        assert collection.request == request
        assert collection.domain  == subject

        assert collection.name is None
        assert collection.type is None

    def test_records_filters_on_name(self, subject):
        collection = subject.records('www')

        assert collection.name == 'www'
        assert collection.type is None

    def test_records_filters_on_blank_name(self, subject):
        collection = subject.records('')

        assert collection.name == ''
        assert collection.type is None

    def test_records_filters_on_type(self, subject):
        collection = subject.records(type = 'A')

        assert collection.name is None
        assert collection.type == 'A'

    def test_record_invokes_finder_with_name(self, mocker, subject):
        finder = mocker.stub()
        finder.return_value = 'record'

        dnsimple.record_collection.RecordCollection.find = finder

        assert subject.record('www') == 'record'

        finder.assert_called_once_with('www', None)

    def test_record_invokes_finder_with_name_and_on_type(self, mocker, subject):
        finder = mocker.stub()

        dnsimple.record_collection.RecordCollection.find = finder

        subject.record('', type = 'A')

        finder.assert_called_once_with('', 'A')

    def test_delete_removes_domain(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'delete')
        subject = Domain(request, {'name':'example.com'})

        assert subject.delete() is True

        method.assert_called_once_with('domains/example.com')

    def test_delete_returns_false_when_removal_fails(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'delete', success = False)
        subject = Domain(request, {'name':'example.com'})

        assert subject.delete() is False

    def test_not_equal_when_no_ids(self, request):
        a = Domain(request, {})
        b = Domain(request, {})

        assert a != b

    def test_not_equal_when_only_one_id(self, request):
        a = Domain(request, {'id': 1})
        b = Domain(request, {})

        assert a != b

    def test_not_equal_when_ids_differ(self, request):
        a = Domain(request, {'id': 1})
        b = Domain(request, {'id': 2})

        assert a != b

    def test_equal_when_ids_are_the_same(self, request):
        a = Domain(request, {'id': 1})
        b = Domain(request, {'id': 1})

        assert a == b
