import pytest

from ..context         import dnsimple
from ..request_helper  import RequestHelper, request

from dnsimple.record import Record
from dnsimple.domain import Domain

@pytest.fixture
def domain(request):
    return Domain(request, {'name':'foo.com'})

@pytest.fixture
def subject(request, domain):
    return Record(request, domain, {'id': 1})

class TestRecord(RequestHelper, object):
    def test_assign_assigns_attributes(self, subject):
        subject.assign({'name': 'www'})

        assert subject.id   == 1
        assert subject.name == 'www'

    def test_update_sends_update_request(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'put', data = {})
        subject = Record(request, domain, {'name': 'www', 'id': 1})

        result = subject.update({'name':'other'})

        method.assert_called_once_with('domains/foo.com/records/1', {'record': {'name':'other'}})

        assert result is True

    def test_update_returns_false_when_request_fails(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'put', success = False, data = {})
        subject = Record(request, domain, {'name': 'www', 'id': 1})

        assert subject.update({}) is False

    def test_update_assigns_attributes(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'put', data = {})
        subject = Record(request, domain, {'name': 'www', 'id': 1})

        subject.update({'name':'other'})

        assert subject.name == 'other'

    def test_delete_removes_record_from_domain(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'delete', data = {})
        subject = Record(request, domain, {'name': 'www', 'id': 1})

        result = subject.delete()

        method.assert_called_once_with('domains/foo.com/records/1')

        assert result is True

    def test_delete_returns_false_when_removal_fails(self, mocker, request, domain):
        method  = self.stub_request(mocker, request, method_name = 'delete', success = False)
        subject = Record(request, domain, {'name': 'www', 'id': 1})

        assert subject.delete() is False

    def test_to_dict_returns_attributes(self, request, domain):
        subject = Record(request, domain, {
            "id"           : 1,
            "content"      : "ns1.dnsimple.com",
            "created_at"   : "2016-08-01T00:00:00.000Z",
            "domain_id"    : 24819,
            "name"         : "Name",
            "parent_id"    : 2,
            "prio"         : 30,
            "record_type"  : "NS",
            "system_record": True,
            "ttl"          : 3600,
            "updated_at"   : "2016-08-01T00:00:00.000Z"
        })

        assert subject.to_dict() == {
            "id"           : 1,
            "content"      : "ns1.dnsimple.com",
            "created_at"   : "2016-08-01T00:00:00.000Z",
            "domain_id"    : 24819,
            "name"         : "Name",
            "parent_id"    : 2,
            "prio"         : 30,
            "record_type"  : "NS",
            "system_record": True,
            "ttl"          : 3600,
            "updated_at"   : "2016-08-01T00:00:00.000Z"
        }

    def test_not_equal_when_no_ids(self, request, domain):
        a = Record(request, domain, {})
        b = Record(request, domain, {})

        assert a != b

    def test_not_equal_when_only_one_id(self, request, domain):
        a = Record(request, domain, {'id': 1})
        b = Record(request, domain, {})

        assert a != b

    def test_not_equal_when_ids_differ(self, request, domain):
        a = Record(request, domain, {'id': 1})
        b = Record(request, domain, {'id': 2})

        assert a != b

    def test_equal_when_ids_are_the_same(self, request, domain):
        a = Record(request, domain, {'id': 1})
        b = Record(request, domain, {'id': 1})

        assert a == b
