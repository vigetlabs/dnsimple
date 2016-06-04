import pytest

from .context import dnsimple

from dnsimple.credentials       import Credentials
from dnsimple.domain            import Domain
from dnsimple.record            import Record
from dnsimple.response          import Response
from dnsimple.record_collection import RecordCollection

@pytest.fixture
def credentials():
    return Credentials()

@pytest.fixture
def domain(credentials):
    return Domain(credentials, {'name':'foo.com'})

@pytest.fixture
def subject(credentials, domain):
    return RecordCollection(credentials, domain)

class TestRecordCollection:
    def test_request_creates_request_with_credentials(self, subject, credentials):
        request = subject.request()

        assert isinstance(request, dnsimple.request.Request)
        assert request.credentials == credentials

    def test_to_dict_returns_condensed_attribute_collection_on_success(self, mocker, subject, credentials):
        response = Response()
        response.to_dict = lambda: [{'record': {'name':'www'}}]

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'get', request)

        result = subject.to_dict()

        request.assert_called_once_with('domains/foo.com/records')

        assert result == [{'name':'www'}]

    def test_to_dict_returns_empty_array_on_failure(self, mocker, subject, credentials):
        response = Response()
        response.was_successful = lambda: False

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'get', request)

        assert subject.to_dict() == []

    def test_all_returns_empty_collection_when_no_records(self, mocker, subject):
        mocker.patch.object(subject, 'to_dict', lambda: [])
        assert len(subject.all()) == 0

    def test_all_returns_collection_of_records(self, mocker, subject):
        mocker.patch.object(subject, 'to_dict', lambda: [{'name':'wwww'}])

        records = subject.all()

        assert len(records) == 1
        assert isinstance(records[0], dnsimple.record.Record)

    def test_find_returns_none_when_there_are_no_records(self, mocker, subject):
        mocker.patch.object(subject, 'all', lambda: [])
        assert subject.find('www') is None

    def test_find_returns_none_when_the_record_name_does_not_match(self, mocker, subject):
        mocker.patch.object(subject, 'all', lambda: [Record(credentials, domain, {'name':'www', 'id':1})])
        assert subject.find('sub') is None

    def test_find_returns_non_when_the_record_id_does_not_match(self, mocker, subject):
        mocker.patch.object(subject, 'all', lambda: [Record(credentials, domain, {'name':'www', 'id':2})])
        assert subject.find(1) is None

    def test_find_returns_matching_record_by_name(self, mocker, subject):
        record = Record(credentials, domain, {'name':'www', 'id':1})

        mocker.patch.object(subject, 'all', lambda: [record])
        assert subject.find('www') == record

    def test_find_returns_matching_record_by_id(self, mocker, subject):
        record = Record(credentials, domain, {'name':'www', 'id':1})

        mocker.patch.object(subject, 'all', lambda: [record])
        assert subject.find(1) == record

    def test_iteration_over_records(self, mocker, subject):
        records = []
        record  = Record(credentials, domain, {'name':'wwww', 'id':1})

        mocker.patch.object(subject, 'all', lambda: [record])

        for record in subject.all():
            records.append(record)

        assert records == [record]

    def test_add_creates_new_record(self, mocker, subject):
        response = Response()
        response.was_successful = lambda: True
        response.to_dict        = lambda: {'record': {'name':'www'}}

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'post', request)

        record = subject.add({'name':'www'})

        request.assert_called_once_with('domains/foo.com/records', {'record': {'name':'www'}})

        assert isinstance(record, dnsimple.record.Record)
        assert record.name == 'www'

    def test_add_returns_none_when_add_is_unsuccessful(self, mocker, subject):
        response = Response()
        response.was_successful = lambda: False

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'post', request)

        assert subject.add({'name':'www'}) is None
