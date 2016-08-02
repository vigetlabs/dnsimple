import pytest

from ..context         import dnsimple
from ..request_helper  import RequestHelper, request

from dnsimple.domain_collection import DomainCollection
from dnsimple.domain            import Domain

@pytest.fixture
def subject(request):
    return DomainCollection(request)

class TestDomainCollection(RequestHelper, object):

    def test_all_returns_empty_collection_when_no_domains(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', data = [])
        subject = DomainCollection(request)

        domains = subject.all()

        method.assert_called_once_with('domains')

        assert domains == []

    def test_all_returns_collection_of_domains(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', data = [{'domain':{'name':'foo.com'}}])
        subject = DomainCollection(request)

        domains = subject.all()

        assert len(domains) == 1

        domain = domains[0]

        assert isinstance(domain, dnsimple.domain.Domain)
        assert domain.name == 'foo.com'

    def test_to_dict_returns_empty_list_when_no_domains(self, mocker, subject):
        mocker.patch.object(subject, 'all', lambda: [])

        assert subject.to_dict() == []

    def test_to_dict_returns_attributes_for_all_domains(self, mocker, subject, request):
        domain_1 = Domain(request, {'name': 'one.com'})
        domain_2 = Domain(request, {'name': 'two.com'})

        mocker.patch.object(subject, 'all', lambda: [domain_1, domain_2])

        assert subject.to_dict() == [{'name':'one.com'}, {'name':'two.com'}]

    def test_find_by_name_returns_none_when_the_domain_does_not_exist(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', success = False)
        subject = DomainCollection(request)

        assert subject.find('foo.com') is None

    def test_find_by_id_returns_none_when_the_domain_does_not_exist(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', success = False, data = {'message':'domain `1` not found'})
        subject = DomainCollection(request)

        assert subject.find(1) is None

    def test_find_returns_matching_domain_by_name(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', data = {'domain': {'name':'foo.com'}})
        subject = DomainCollection(request)

        domain = subject.find('foo.com')

        method.assert_called_once_with('domains/foo.com')

        assert isinstance(domain, dnsimple.domain.Domain)
        assert domain.name == 'foo.com'

    def test_find_returns_matching_domain_by_id(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', data = {'domain': {'name':'foo.com'}})
        subject = DomainCollection(request)

        domain = subject.find(1)

        method.assert_called_once_with('domains/1')

        assert isinstance(domain, dnsimple.domain.Domain)
        assert domain.name == 'foo.com'

    def test_iteration_over_domains(self, mocker, request, subject):
        domains = []
        domain  = Domain(request, {'name':'foo.com', 'id':1})

        mocker.patch.object(subject, 'all', lambda: [domain])

        for domain in subject.all():
            domains.append(domain)

        assert domains == [domain]

    def test_add_creates_new_domain_record(self, mocker, request, subject):
        method = self.stub_request(mocker, request, method_name = 'post', data = {'domain': {'name':'foo.com'}})

        domain = subject.add({'name':'foo.com'})

        method.assert_called_once_with('domains', {'domain': {'name':'foo.com'}})

        assert isinstance(domain, dnsimple.domain.Domain)
        assert domain.name == 'foo.com'

    def test_add_returns_none_when_add_is_unsuccessful(self, mocker, request, subject):
        method = self.stub_request(mocker, request, method_name = 'post', data = {}, success = False)

        assert subject.add({'name':'foo.com'}) is None
