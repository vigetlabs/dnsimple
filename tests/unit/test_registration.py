from ..context        import dnsimple
from ..request_helper import RequestHelper, request

from dnsimple.registration import Registration
from dnsimple.models      import Contact

class TestRegistration(RequestHelper, object):

    def test_add_registers_new_domain(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'post', success = True, data = {'domain': {'id': 1, 'name':'foo.com'}})
        subject = Registration(request)
        contact = Contact(request, {'id': 99})

        domain = subject.add('foo.com', contact)

        assert isinstance(domain, dnsimple.models.Domain)
        assert domain.id == 1
        assert domain.name == 'foo.com'

        method.assert_called_once_with('domain_registrations', {'domain': {'name': 'foo.com', 'registrant_id': 99}})

    def test_add_returns_none_when_registration_fails(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'post', success = False)
        subject = Registration(request)
        contact = Contact(request, {})

        assert subject.add('foo.com', contact) is None
