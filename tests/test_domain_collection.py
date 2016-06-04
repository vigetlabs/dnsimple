import pytest

from .context import dnsimple

from dnsimple.domain_collection import DomainCollection
from dnsimple.credentials       import Credentials
from dnsimple.response          import Response
from dnsimple.domain            import Domain

@pytest.fixture
def credentials():
    return dnsimple.credentials.Credentials()

@pytest.fixture
def subject(credentials):
    return DomainCollection(credentials)

class TestDomainCollection:

    def test_request_creates_request_with_credentials(self, subject, credentials):
        request = subject.request()

        assert isinstance(request, dnsimple.request.Request)
        assert request.credentials == credentials

    def test_to_dict_returns_condensed_attribute_collection_on_success(self, mocker, subject, credentials):
        response = Response()
        response.to_dict = lambda: [{'domain': {'name':'foo.com'}}]

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'get', request)

        result = subject.to_dict()

        request.assert_called_once_with('domains')

        assert result == [{'name':'foo.com'}]

    def test_to_dict_returns_empty_array_on_failure(self, mocker, subject, credentials):
        response = Response()
        response.was_successful = lambda: False

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'get', request)

        assert subject.to_dict() == []

    def test_all_returns_empty_collection_when_no_domains(self, mocker, subject):
        mocker.patch.object(subject, 'to_dict', lambda: [])
        assert len(subject.all()) == 0

    def test_all_returns_collection_of_domains(self, mocker, subject):
        mocker.patch.object(subject, 'to_dict', lambda: [{'name':'foo.com'}])

        domains = subject.all()

        assert len(domains) == 1
        assert isinstance(domains[0], dnsimple.domain.Domain)

    def test_find_returns_none_when_there_are_no_domains(self, mocker, subject):
        mocker.patch.object(subject, 'all', lambda: [])
        assert subject.find('foo.com') is None

    def test_find_returns_none_when_the_domain_name_does_not_match(self, mocker, subject):
        mocker.patch.object(subject, 'all', lambda: [Domain(credentials, {'name':'bar.com', 'id':1})])
        assert subject.find('foo.com') is None

    def test_find_returns_non_when_the_domain_id_does_not_match(self, mocker, subject):
        mocker.patch.object(subject, 'all', lambda: [Domain(credentials, {'name':'foo.com', 'id':2})])
        assert subject.find(1) is None

    def test_find_returns_matching_domain_by_name(self, mocker, subject):
        domain = Domain(credentials, {'name':'foo.com', 'id':1})

        mocker.patch.object(subject, 'all', lambda: [domain])
        assert subject.find('foo.com') == domain

    def test_find_returns_matching_domain_by_id(self, mocker, subject):
        domain = Domain(credentials, {'name':'foo.com', 'id':1})

        mocker.patch.object(subject, 'all', lambda: [domain])
        assert subject.find(1) == domain

    def test_iteration_over_domains(self, mocker, subject):
        domains = []
        domain  = Domain(credentials, {'name':'foo.com', 'id':1})

        mocker.patch.object(subject, 'all', lambda: [domain])

        for domain in subject.all():
            domains.append(domain)

        assert domains == [domain]

    def test_add_creates_new_domain_record(self, mocker, subject):
        response = Response()
        response.was_successful = lambda: True
        response.to_dict        = lambda: {'domain': {'name':'foo.com'}}

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'post', request)

        domain = subject.add({'name':'foo.com'})

        request.assert_called_once_with('domains', {'domain': {'name':'foo.com'}})

        assert isinstance(domain, dnsimple.domain.Domain)
        assert domain.name == 'foo.com'

    def test_add_returns_none_when_add_is_unsuccessful(self, mocker, subject):
        response = Response()
        response.was_successful = lambda: False

        request = mocker.stub()
        request.return_value = response

        subject.request = lambda: other

        other = dnsimple.request.Request(credentials)
        mocker.patch.object(other, 'post', request)

        assert subject.add({'name':'foo.com'}) is None
