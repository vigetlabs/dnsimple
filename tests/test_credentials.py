from .context import dnsimple

from dnsimple.credentials import Credentials

class TestCredentials:
    def test_is_valid_is_false_by_default(self):
        subject = Credentials()
        assert subject.is_valid() is False

    def test_is_valid_is_false_when_partial_auth(self):
        subject = Credentials(email = 'user@host.com')
        assert subject.is_valid() is False

    def test_is_valid_is_true_when_user_token_auth(self):
        subject = Credentials(email = 'user@host.com', user_token = 'toke')
        assert subject.is_valid() is True

    def test_is_valid_is_true_when_basic_auth(self):
        subject = Credentials(email = 'user@host.com', password = 'password')
        assert subject.is_valid() is True

    def test_is_basic_auth_is_false_by_default(self):
        subject = Credentials()
        assert subject.is_basic_auth() is False

    def test_is_basic_auth_is_false_when_using_token_auth(self):
        subject = Credentials(email = 'user@host.com', user_token = 'toke')
        assert subject.is_basic_auth() is False

    def test_is_basic_auth_is_true_when_using_basic_auth(self):
        subject = Credentials(email = 'user@host.com', password = 'password')
        assert subject.is_basic_auth() is True

    def test_is_token_auth_is_false_by_default(self):
        subject = Credentials()
        assert subject.is_token_auth() is False

    def test_is_token_auth_is_false_when_using_basic_auth(self):
        subject = Credentials(email = 'user@host.com', password = 'password')
        assert subject.is_token_auth() is False

    def test_is_token_auth_is_true_when_using_token_auth(self):
        subject = Credentials(email = 'user@host.com', user_token = 'toke')
        assert subject.is_token_auth() is True
