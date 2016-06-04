import pytest

from .context import dnsimple

from dnsimple.domain      import Domain
from dnsimple.credentials import Credentials
from dnsimple.record_collection import RecordCollection

@pytest.fixture
def credentials():
    return Credentials()

class TestDomain:
    def test_to_dict_returns_attributes(self):
        subject = Domain(credentials, {'key':'value'})
        assert subject.to_dict() == {'key':'value'}

    def test_records_creates_instance_of_collection(self):
        subject     = Domain(credentials, {})

        collection = subject.records()

        assert isinstance(collection, RecordCollection)

        assert collection.domain      == subject
        assert collection.credentials == credentials
