import pytest

from .context import dnsimple
from .helper  import TestHelper

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

class TestRecordCollection(TestHelper, object):
    def test_request_creates_request_with_credentials(self, subject, credentials):
        request = subject.request()

        assert isinstance(request, dnsimple.request.Request)
        assert request.credentials == credentials

    def test_all_returns_empty_collection_when_no_records(self, mocker, subject):
        response = self.stub_response([])
        request  = self.stub_request(subject, mocker, response)

        records = subject.all()

        request.assert_called_once_with('domains/foo.com/records', {})

        assert records == []

    def test_all_filters_results_by_name(self, mocker, credentials, domain):
        subject = RecordCollection(credentials, domain, 'www')

        response = self.stub_response([])
        request  = self.stub_request(subject, mocker, response)

        subject.all()

        request.assert_called_once_with('domains/foo.com/records', {'name':'www'})

    def test_all_filters_results_by_empty_name(self, mocker, credentials, domain):
        subject = RecordCollection(credentials, domain, '')

        response = self.stub_response([])
        request  = self.stub_request(subject, mocker, response)

        subject.all()

        request.assert_called_once_with('domains/foo.com/records', {'name':''})

    def test_all_filters_results_by_type(self, mocker, credentials, domain):
        subject = RecordCollection(credentials, domain, type = 'NS')

        response = self.stub_response([])
        request  = self.stub_request(subject, mocker, response)

        subject.all()

        request.assert_called_once_with('domains/foo.com/records', {'type':'NS'})

    def test_all_filters_results_by_name_and_type(self, mocker, credentials, domain):
        subject = RecordCollection(credentials, domain, 'www', type = 'A')

        response = self.stub_response([])
        request  = self.stub_request(subject, mocker, response)

        subject.all()

        request.assert_called_once_with('domains/foo.com/records', {'name':'www','type':'A'})

    def test_all_returns_collection_of_records(self, mocker, subject):
        response = self.stub_response([{'record':{'name':'www'}}])
        request  = self.stub_request(subject, mocker, response)

        records = subject.all()

        assert len(records) == 1

        record = records[0]

        assert isinstance(record, dnsimple.record.Record)
        assert record.name == 'www'

    def test_where_returns_new_instance_with_filters(self, subject):
        filtered = subject.where(name = 'www', type = 'A')

        assert isinstance(filtered, RecordCollection)
        assert filtered.name == 'www'
        assert filtered.type == 'A'

        assert filtered.name != subject.name
        assert filtered.type != subject.type

    def test_to_dict_returns_empty_list_when_no_domains(self, mocker, subject):
        mocker.patch.object(subject, 'all', lambda: [])
        assert subject.to_dict() == []

    def test_to_dict_returns_attributes_for_all_records(self, mocker, subject, domain, credentials):
        record_1 = Record(credentials, domain, {'name':'one'})
        record_2 = Record(credentials, domain, {'name':'two'})

        mocker.patch.object(subject, 'all', lambda: [record_1, record_2])

        assert subject.to_dict() == [{'name':'one'},{'name':'two'}]

    def stub_filter(self, mocker):
        credentials = Credentials()
        domain      = Domain(credentials, {})

        finder = mocker.stub()
        finder.return_value = []

        filtered = RecordCollection(credentials, domain)
        mocker.patch.object(filtered, 'all', finder)

        where_filter = mocker.stub()
        where_filter.return_value = filtered

        return where_filter

    def test_find_returns_none_when_the_record_id_does_not_match(self, mocker, subject, credentials, domain):
        response = self.stub_response({'message':'record with ID 1 not found'}, success = False)
        request  = self.stub_request(subject, mocker, response)

        where_filter = self.stub_filter(mocker)
        mocker.patch.object(subject, 'where', where_filter)

        record = Record(credentials, domain, {'name':'www', 'id':2})

        assert subject.find(1) is None

        where_filter.assert_called_once_with('1', None)

    # def test_find_returns_matching_record_with_numeric_hostname(self, mocker, subject):
    #     response = self.stub_response({'message':'record with ID 1 not found'}, success = False)
    #     request  = self.stub_request(subject, mocker, response)
    #
    #     record = Record(credentials, domain, {'name':'1', 'id':2})
    #
    #     mocker.patch.object(subject, 'all', lambda: [record])
    #
    #     assert subject.find(1) == record
    #
    # def test_find_returns_matching_record_by_name(self, mocker, subject):
    #     record = Record(credentials, domain, {'name':'www', 'id':1})
    #
    #     mocker.patch.object(subject, 'all', lambda: [record])
    #     assert subject.find('www') == record
    #
    def test_find_returns_matching_record_by_id(self, mocker, subject):
        response = self.stub_response({'record':{'name':'foo.com', 'id':1}})
        request  = self.stub_request(subject, mocker, response)

        record = subject.find(1)

        request.assert_called_once_with('domains/foo.com/records/1')

        assert isinstance(record, dnsimple.record.Record)
        assert record.name == 'foo.com'
        assert record.id   == 1

    def test_iteration_over_records(self, mocker, subject):
        records = []
        record  = Record(credentials, domain, {'name':'wwww', 'id':1})

        mocker.patch.object(subject, 'all', lambda: [record])

        for record in subject.all():
            records.append(record)

        assert records == [record]

    def test_add_creates_new_record(self, mocker, subject):
        response = self.stub_response({'record': {'name':'www'}})
        request  = self.stub_request(subject, mocker, response, method = 'post')

        record = subject.add({'name':'www'})

        request.assert_called_once_with('domains/foo.com/records', {'record': {'name':'www'}})

        assert isinstance(record, dnsimple.record.Record)
        assert record.name == 'www'

    def test_add_returns_none_when_add_is_unsuccessful(self, mocker, subject):
        response = self.stub_response({}, success = False)
        request  = self.stub_request(subject, mocker, response, method = 'post')

        assert subject.add({'name':'www'}) is None
