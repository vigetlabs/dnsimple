import pytest

from .context import dnsimple

from dnsimple.domain            import Domain
from dnsimple.credentials       import Credentials
from dnsimple.record_collection import RecordCollection

@pytest.fixture
def credentials():
    return Credentials()

class TestDomain:
    def test_to_dict_returns_attributes(self):
        subject = Domain(credentials, {'key':'value'})
        assert subject.to_dict() == {'key':'value'}

    def test_records_creates_instance_of_collection(self):
        subject    = Domain(credentials, {})
        collection = subject.records()

        assert isinstance(collection, RecordCollection)

        assert collection.domain      == subject
        assert collection.credentials == credentials

    def test_record_returns_single_record(self, mocker):
        original_find = dnsimple.record_collection.RecordCollection.find

        finder = mocker.stub()
        finder.return_value = 'record'

        dnsimple.record_collection.RecordCollection.find = finder

        subject = Domain(credentials, {})
        assert subject.record('www') == 'record'

        finder.assert_called_once_with('www')

        dnsimple.record_collection.RecordCollection.find = original_find
