import pytest

from .context import dnsimple
from .helper  import TestHelper

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

class TestDomainCollection(TestHelper, object):

    def test_request_creates_request_with_credentials(self, subject, credentials):
        request = subject.request()

        assert isinstance(request, dnsimple.request.Request)
        assert request.credentials == credentials

    def test_to_dict_returns_condensed_attribute_collection_on_success(self, mocker, subject, credentials):
        response = self.stub_response([{'domain': {'name':'foo.com'}}])
        request  = self.stub_request(subject, mocker, response)

        result = subject.to_dict()

        request.assert_called_once_with('domains')

        assert result == [{'name':'foo.com'}]

    def test_to_dict_returns_empty_array_on_failure(self, mocker, subject, credentials):
        response = self.stub_response({}, success = False)
        request  = self.stub_request(subject, mocker, response)

        assert subject.to_dict() == []

    def test_all_returns_empty_collection_when_no_domains(self, mocker, subject):
        mocker.patch.object(subject, 'to_dict', lambda: [])
        assert len(subject.all()) == 0

    def test_all_returns_collection_of_domains(self, mocker, subject):
        mocker.patch.object(subject, 'to_dict', lambda: [{'name':'foo.com'}])

        domains = subject.all()

        assert len(domains) == 1
        assert isinstance(domains[0], dnsimple.domain.Domain)

    def test_find_by_name_returns_none_when_the_domain_does_not_exist(self, mocker, subject):
        response = self.stub_response({'message':'domain foo.com not found'}, success = False)
        request  = self.stub_request(subject, mocker, response)

        assert subject.find('foo.com') is None

    def test_find_by_id_returns_none_when_the_domain_does_not_exist(self, mocker, subject):
        response = self.stub_response({'message':'domain `1` not found'}, success = False)
        request  = self.stub_request(subject, mocker, response)

        assert subject.find(1) is None

    def test_find_returns_matching_domain_by_name(self, mocker, subject):
        response = self.stub_response({'domain': {'name':'foo.com'}})
        request  = self.stub_request(subject, mocker, response)

        domain = subject.find('foo.com')

        request.assert_called_once_with('domains/foo.com')

        assert isinstance(domain, dnsimple.domain.Domain)
        assert domain.name == 'foo.com'

    def test_find_returns_matching_domain_by_id(self, mocker, subject):
        response = self.stub_response({'domain': {'name':'foo.com'}})
        request  = self.stub_request(subject, mocker, response)

        domain = subject.find(1)

        request.assert_called_once_with('domains/1')

        assert isinstance(domain, dnsimple.domain.Domain)
        assert domain.name == 'foo.com'

    def test_iteration_over_domains(self, mocker, subject):
        domains = []
        domain  = Domain(credentials, {'name':'foo.com', 'id':1})

        mocker.patch.object(subject, 'all', lambda: [domain])

        for domain in subject.all():
            domains.append(domain)

        assert domains == [domain]

    def test_add_creates_new_domain_record(self, mocker, subject):
        response = self.stub_response({'domain': {'name':'foo.com'}})
        request  = self.stub_request(subject, mocker, response, method = 'post')

        domain = subject.add({'name':'foo.com'})

        request.assert_called_once_with('domains', {'domain': {'name':'foo.com'}})

        assert isinstance(domain, dnsimple.domain.Domain)
        assert domain.name == 'foo.com'

    def test_add_returns_none_when_add_is_unsuccessful(self, mocker, subject):
        response = self.stub_response({}, success = False)
        request  = self.stub_request(subject, mocker, response, method = 'post')

        assert subject.add({'name':'foo.com'}) is None
