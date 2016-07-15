import pytest

from .context import dnsimple, fixture_path

from dnsimple.client import Client

class TestClient:

    def test_constructor_raises_errors_when_improperly_configured(self):
        with pytest.raises(dnsimple.credentials.InvalidCredentialsException) as ex:
            Client(email = 'user@host.com')

        assert 'Invalid credentials supplied' in str(ex.value)

    def test_constructor_raises_errors_when_no_credentials_found(self):
        with pytest.raises(dnsimple.credentials.InvalidCredentialsException):
            Client(credentials_search_paths = fixture_path('credentials'), credentials_filename = 'missing')

    def test_constructor_configures_credentials_for_token_authentication(self):
        subject = Client(email = 'user@host.com', user_token = 'toke')

        assert subject.credentials.email      == 'user@host.com'
        assert subject.credentials.user_token == 'toke'

    def test_constructor_configures_credentials_for_password_authentication(self):
        subject = Client(email = 'user@host.com', password = 'password')

        assert subject.credentials.email    == 'user@host.com'
        assert subject.credentials.password == 'password'

    def test_constructor_configures_credentials_from_configuration_file(self):
        subject = Client(credentials_search_paths = [fixture_path('credentials')], credentials_filename = 'basic')

        assert subject.credentials.email      == 'user@host.com'
        assert subject.credentials.user_token == 'token'
        assert subject.credentials.password   == 'password'

    def test_constructor_defaults_sandbox_to_false(self):
        subject = Client(email = 'user@host.com', password = 'password')
        assert dnsimple.request.Request.sandbox is False

    def test_constructor_enables_sandbox(self):
        subject = Client(sandbox = True, email = 'user@host.com', password = 'password')
        assert dnsimple.request.Request.sandbox is True

    def test_domains_returns_domain_collection(self):
        subject = Client(email = 'user@host.com', password = 'password')
        domains = subject.domains()

        assert isinstance(domains, dnsimple.domain_collection.DomainCollection)
        assert domains.credentials == subject.credentials

    def test_domain_returns_single_domain(self, mocker):
        original_find = dnsimple.domain_collection.DomainCollection.find

        finder = mocker.stub()
        finder.return_value = 'domain'

        dnsimple.domain_collection.DomainCollection.find = finder

        subject = Client(email = 'user@host.com', password = 'password')
        assert subject.domain('foo.com') == 'domain'

        finder.assert_called_once_with('foo.com')

        dnsimple.domain_collection.DomainCollection.find = original_find
