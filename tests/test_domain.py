import pytest

from .context import dnsimple

from dnsimple.domain            import Domain
from dnsimple.credentials       import Credentials
from dnsimple.record_collection import RecordCollection

@pytest.fixture
def credentials():
    return Credentials()

class TestDomain:
    def setup_method(self, method):
        self.original_find = dnsimple.record_collection.RecordCollection.find

    def teardown_method(self, method):
        dnsimple.record_collection.RecordCollection.find = self.original_find

    def test_to_dict_returns_attributes(self):
        subject = Domain(credentials, {'key':'value'})
        assert subject.to_dict() == {'key':'value'}

    def test_records_creates_instance_of_collection(self):
        subject    = Domain(credentials, {})
        collection = subject.records()

        assert isinstance(collection, RecordCollection)

        assert collection.domain      == subject
        assert collection.credentials == credentials

        assert collection.name is None
        assert collection.type is None

    def test_records_filters_on_name(self):
        subject    = Domain(credentials, {})
        collection = subject.records('www')

        assert collection.name == 'www'
        assert collection.type is None

    def test_records_filters_on_blank_name(self):
        subject    = Domain(credentials, {})
        collection = subject.records('')

        assert collection.name == ''
        assert collection.type is None

    def test_records_filters_on_type(self):
        subject    = Domain(credentials, {})
        collection = subject.records(type = 'A')

        assert collection.name is None
        assert collection.type == 'A'

    def test_record_returns_single_record(self, mocker):
        finder = mocker.stub()
        finder.return_value = 'record'

        dnsimple.record_collection.RecordCollection.find = finder

        subject = Domain(credentials, {})
        assert subject.record('www') == 'record'

        finder.assert_called_once_with('www', None)

    def test_record_filters_on_type(self, mocker):
        finder = mocker.stub()

        dnsimple.record_collection.RecordCollection.find = finder

        subject = Domain(credentials, {})
        subject.record('', type = 'A')

        finder.assert_called_once_with('', 'A')
