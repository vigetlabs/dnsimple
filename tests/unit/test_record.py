import pytest

from ..context import dnsimple

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

class TestRecord:
    def test_request_creates_request_with_credentials(self, subject, credentials):
        request = subject.request()

        assert isinstance(request, dnsimple.request.Request)
        assert request.credentials == credentials

    def test_delete_removes_record_from_domain(self, mocker, subject):
        response = dnsimple.response.Response()
        response.was_successful = lambda: True

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'delete', request)

        result = subject.delete()

        request.assert_called_once_with('domains/foo.com/records/1')

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

    def test_to_dict_returns_attributes(self, credentials, domain):
        subject = Record(credentials, domain, {'key':'value'})
        assert subject.to_dict() == {'key':'value'}
