import pytest

from .context import dnsimple

from dnsimple.domain            import Domain
from dnsimple.credentials       import Credentials
from dnsimple.record_collection import RecordCollection

@pytest.fixture
def credentials():
    return Credentials()

@pytest.fixture
def subject():
    return Domain(credentials, {'name':'example.com'})

class TestDomain:
    def setup_method(self, method):
        self.original_find = dnsimple.record_collection.RecordCollection.find

    def teardown_method(self, method):
        dnsimple.record_collection.RecordCollection.find = self.original_find

    def test_to_dict_returns_attributes(self):
        subject = Domain(credentials, {'key':'value'})
        assert subject.to_dict() == {'key':'value'}

    def test_records_creates_instance_of_collection(self, subject):
        collection = subject.records()

        assert isinstance(collection, RecordCollection)

        assert collection.domain      == subject
        assert collection.credentials == credentials

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

    def test_record_returns_single_record(self, mocker, subject):
        finder = mocker.stub()
        finder.return_value = 'record'

        dnsimple.record_collection.RecordCollection.find = finder

        assert subject.record('www') == 'record'

        finder.assert_called_once_with('www', None)

    def test_record_filters_on_type(self, mocker, subject):
        finder = mocker.stub()

        dnsimple.record_collection.RecordCollection.find = finder

        subject.record('', type = 'A')

        finder.assert_called_once_with('', 'A')

    def test_delete_removes_domain(self, mocker, subject):
        response = dnsimple.response.Response()
        response.was_successful = lambda: True

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'delete', request)

        result = subject.delete()

        request.assert_called_once_with('domains/example.com')

        assert result is True

    def test_delete_returns_false_when_removal_fails(self, mocker, subject):
        response = dnsimple.response.Response()
        response.was_successful = lambda: False

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'delete', request)

        assert subject.delete() is False

