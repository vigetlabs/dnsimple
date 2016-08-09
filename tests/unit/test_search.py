from ..context        import dnsimple
from ..request_helper import RequestHelper, request

from dnsimple.search import Search

class TestSearch(RequestHelper, object):

    def test_find_fetches_registered_domain_registration_record(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', data = {'available': False}, success = True)
        subject = Search(request)

        status = subject.find('google.com')

        method.assert_called_once_with('domains/google.com/check')

        assert isinstance(status, dnsimple.models.Status)
        assert not status.available

    def test_find_fetches_unregistered_domain_registration_record(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'get', data = {'available': True}, success = False)
        subject = Search(request)

        status = subject.find('available.com')

        assert isinstance(status, dnsimple.models.Status)
        assert status.available
