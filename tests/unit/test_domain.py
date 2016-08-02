import pytest

from ..context         import dnsimple
from ..request_helper  import RequestHelper

from dnsimple.domain            import Domain
from dnsimple.record_collection import RecordCollection

@pytest.fixture
def request():
    return dnsimple.request.Request(dnsimple.credentials.Credentials())

@pytest.fixture
def subject(request):
    return Domain(request, {'name':'example.com'})

class TestDomain(RequestHelper, object):

    def setup_method(self, method):
        self.original_find = dnsimple.record_collection.RecordCollection.find

    def teardown_method(self, method):
        dnsimple.record_collection.RecordCollection.find = self.original_find

    def test_assign_assigns_attributes(self, subject):
        subject.assign({'name': 'foo.com'})

        assert subject.name == 'foo.com'

    def test_to_dict_returns_attributes(self, subject):
        assert subject.to_dict() == {'name':'example.com'}

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