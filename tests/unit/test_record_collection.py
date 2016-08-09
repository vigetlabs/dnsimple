import pytest

from ..context         import dnsimple
from ..request_helper  import RequestHelper, request

from dnsimple.models            import Domain, Record
from dnsimple.collections import RecordCollection

@pytest.fixture
def domain(request):
    return Domain(request, {'name':'foo.com'})

@pytest.fixture
def subject(request, domain):
    return RecordCollection(request, domain)

class TestRecordCollection(RequestHelper, object):

    def stub_filter(self, mocker, subject, return_value):
        request      = dnsimple.connection.Request(dnsimple.credentials.Credentials())
        domain       = Domain(request, {})
        filtered     = RecordCollection(request, domain)
        finder       = mocker.stub()
        where_filter = mocker.stub()

        finder.return_value = return_value

        mocker.patch.object(filtered, 'all', finder)

        where_filter.return_value = filtered

        mocker.patch.object(subject, 'where', where_filter)

        return where_filter

    def test_all_returns_empty_collection_when_no_records(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'get', data = [])
        subject = RecordCollection(request, domain)

        records = subject.all()

        method.assert_called_once_with('domains/foo.com/records', {})

        assert records == []

    def test_all_filters_results_by_name(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'get', data = [])
        subject = RecordCollection(request, domain, 'www')

        subject.all()

        method.assert_called_once_with('domains/foo.com/records', {'name':'www'})

    def test_all_filters_results_by_empty_name(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'get', data = [])
        subject = RecordCollection(request, domain, '')

        subject.all()

        method.assert_called_once_with('domains/foo.com/records', {'name':''})

    def test_all_filters_results_by_type(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'get', data = [])
        subject = RecordCollection(request, domain, type = 'NS')

        subject.all()

        method.assert_called_once_with('domains/foo.com/records', {'type':'NS'})

    def test_all_filters_results_by_name_and_type(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'get', data = [])
        subject = RecordCollection(request, domain, 'www', type = 'A')

        subject.all()

        method.assert_called_once_with('domains/foo.com/records', {'name':'www','type':'A'})

    def test_all_returns_collection_of_records(self, mocker, request, domain):
        self.stub_request(mocker, request, method_name = 'get', data = [{'record':{'name':'www'}}])

        subject = RecordCollection(request, domain)

        records = subject.all()

        assert len(records) == 1

        record = records[0]

        assert isinstance(record, dnsimple.models.Record)
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

    def test_to_dict_returns_attributes_for_all_records(self, mocker, domain, request, subject):
        record_1 = Record(request, domain, {'name':'one'})
        record_2 = Record(request, domain, {'name':'two'})

        mocker.patch.object(subject, 'all', lambda: [record_1, record_2])

        results = subject.to_dict()

        assert isinstance(results, list)
        assert len(results) == 2

        assert isinstance(results[0], dict)
        assert isinstance(results[1], dict)

        assert results[0]['name'] == 'one'
        assert results[1]['name'] == 'two'

    def test_find_returns_none_when_the_record_id_does_not_match(self, mocker, request, domain):
        self.stub_request(mocker, request, method_name = 'get', success = False, data = {'message':'record with ID 1 not found'})

        subject = RecordCollection(request, domain)

        where_filter = self.stub_filter(mocker, subject, [])

        assert subject.find(1) is None

        where_filter.assert_called_once_with('1', None)

    def test_find_returns_matching_record_by_name(self, mocker, subject):
        record = Record(request, domain, {'name':'www', 'id': 1})

        self.stub_filter(mocker, subject, [record])

        assert subject.find('www') == record

    def test_find_raises_exception_when_multiple_results_found(self, mocker, request, domain, subject):
        records = [
            Record(request, domain, {'name':'', 'id': 1}),
            Record(request, domain, {'name':'', 'id': 2})
        ]

        where_filter = self.stub_filter(mocker, subject, records)

        with pytest.raises(dnsimple.collections.MultipleResultsException) as ex:
            subject.find('www')

        assert 'Multiple results returned for query' in str(ex.value)

    def test_find_returns_matching_record_with_numeric_hostname(self, mocker, request, domain):
        self.stub_request(mocker, request, method_name = 'get', success = False, data = {'message':'record with ID 1 not found'})

        record  = Record(request, domain, {'name':'1', 'id': 2})
        subject = RecordCollection(request, domain)

        where_filter = self.stub_filter(mocker, subject, [record])

        assert subject.find(1) == record

    def test_find_returns_matching_record_by_id(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'get', data = {'record':{'name':'foo.com', 'id':1}})
        subject = RecordCollection(request, domain)

        record = subject.find(1)

        method.assert_called_once_with('domains/foo.com/records/1')

        assert isinstance(record, dnsimple.models.Record)
        assert record.name == 'foo.com'
        assert record.id   == 1

    def test_iteration_over_records(self, mocker, request, subject):
        records = []
        record  = Record(request, domain, {'name': 'wwww', 'id': 1})

        mocker.patch.object(subject, 'all', lambda: [record])

        for record in subject.all():
            records.append(record)

        assert records == [record]

    def test_add_creates_new_record(self, mocker, request, domain):
        method = self.stub_request(mocker, request, method_name = 'post', data = {'record': {'name':'www'}})
        subject = RecordCollection(request, domain)

        record = subject.add({'name':'www'})

        method.assert_called_once_with('domains/foo.com/records', {'record': {'name':'www'}})

        assert isinstance(record, dnsimple.models.Record)
        assert record.name == 'www'

    def test_add_returns_none_when_add_is_unsuccessful(self, mocker, request, domain):
        method = self.stub_request(mocker, request, method_name = 'post', success = False, data = {})
        subject = RecordCollection(request, domain)

        assert subject.add({'name':'www'}) is None
