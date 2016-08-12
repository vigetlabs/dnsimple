import pytest

from ..context         import dnsimple, fixture_path
from ..request_helper import RequestHelper, request

from dnsimple.client import Client

class TestClient(RequestHelper, object):

    def test_constructor_raises_errors_when_improperly_configured(self):
        with pytest.raises(dnsimple.credentials.InvalidCredentialsException) as ex:
            Client(email = 'user@host.com')

        assert 'Invalid credentials supplied' in str(ex.value)

    def test_constructor_raises_errors_when_no_credentials_found(self):
        with pytest.raises(dnsimple.credentials.InvalidCredentialsException):
            Client(credentials_search_paths = fixture_path('credentials'), credentials_filename = 'missing')

    def test_constructor_configures_credentials_for_token_authentication(self):
        subject = Client(email = 'user@host.com', user_token = 'toke')

        assert isinstance(subject.request, dnsimple.connection.Request)

        credentials = subject.request.credentials

        assert credentials.email      == 'user@host.com'
        assert credentials.user_token == 'toke'

    def test_constructor_configures_credentials_for_password_authentication(self):
        subject = Client(email = 'user@host.com', password = 'password')

        credentials = subject.request.credentials

        assert credentials.email    == 'user@host.com'
        assert credentials.password == 'password'

    def test_constructor_configures_credentials_for_domain_token_authentication(self):
        subject = Client(domain_token = 'token')
        assert subject.request.credentials.domain_token == 'token'

    def test_constructor_configures_credentials_from_configuration_file(self):
        subject = Client(credentials_search_paths = [fixture_path('credentials')], credentials_filename = 'basic')

        credentials = subject.request.credentials

        assert credentials.email      == 'user@host.com'
        assert credentials.user_token == 'user_token'
        assert credentials.password   == 'password'

    def test_constructor_defaults_sandbox_to_false(self):
        subject = Client(email = 'user@host.com', password = 'password')
        assert subject.request.sandbox is False

    def test_constructor_enables_sandbox(self):
        subject = Client(sandbox = True, email = 'user@host.com', password = 'password')
        assert subject.request.sandbox is True

    def test_transfer_creates_domain_transfer(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'post', success = True, data = {})
        subject = Client(email = 'user@host.com', password = 'password')
        contact = dnsimple.models.Contact(request, {'id': 1})

        subject.request = request

        result = subject.transfer('foo.com', contact)

        method.assert_called_once_with('domain_transfers', {'domain': {'name': 'foo.com', 'registrant_id': 1}})

        assert result == True

    def test_transfer_returns_false_when_transfer_fails(self, mocker, request):
        method  = self.stub_request(mocker, request, method_name = 'post', success = False)
        subject = Client(email = 'user@host.com', password = 'password')
        contact = dnsimple.models.Contact(request, {'id': 1})

        subject.request = request

        result = subject.transfer('foo.com', contact)

        assert result == False
