import pytest

from ..context import dnsimple
from ..helper  import TestHelper

from dnsimple.record      import Record
from dnsimple.credentials import Credentials
from dnsimple.domain      import Domain

@pytest.fixture
def credentials():
    return Credentials()

@pytest.fixture
def domain(credentials):
    return Domain(credentials, {'name':'foo.com'})

@pytest.fixture
def subject(credentials, domain):
    return Record(credentials, domain, {'id':1})

class TestRecord(TestHelper, object):
    def test_assign_assigns_attributes(self, credentials, domain):
        subject = Record(credentials, domain, {})
        subject.assign({'name': 'www'})

        assert subject.name == 'www'

    def test_request_creates_request_with_credentials(self, subject, credentials):
        request = subject.request()

        assert isinstance(request, dnsimple.request.Request)
        assert request.credentials == credentials

    def test_update_sends_update_request(self, mocker, subject):
        response = self.stub_response({})
        request  = self.stub_request(subject, mocker, response, 'put')

        result = subject.update({'name':'other'})

        request.assert_called_once_with('domains/foo.com/records/1', {'record': {'name':'other'}})

        assert result is True

    def test_update_returns_false_when_request_fails(self, mocker, subject):
        response = self.stub_response({}, False)
        request  = self.stub_request(subject, mocker, response, 'put')

        assert subject.update({}) is False

    def test_update_assigns_attributes(self, mocker, subject):
        response = self.stub_response({})
        request  = self.stub_request(subject, mocker, response, 'put')

        subject.name = 'www'

        subject.update({'name':'other'})

        assert subject.name == 'other'

    def test_delete_removes_record_from_domain(self, mocker, subject):
        response = self.stub_response({})
        request  = self.stub_request(subject, mocker, response, 'delete')

        result = subject.delete()

        request.assert_called_once_with('domains/foo.com/records/1')

        assert result is True

    def test_delete_returns_false_when_removal_fails(self, mocker, subject):
        response = self.stub_response(None, False)
        request  = self.stub_request(subject, mocker, response, 'delete')

        assert subject.delete() is False

    def test_to_dict_returns_attributes(self, credentials, domain):
        subject = Record(credentials, domain, {'key':'value'})
        assert subject.to_dict() == {'key':'value'}
