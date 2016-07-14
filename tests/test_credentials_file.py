from .context import dnsimple, fixture_path

from dnsimple.credentials_file import CredentialsFile

class TestCredentialsFile:
    def test_credentials_are_blank_when_no_configuration_file(self):
        subject     = CredentialsFile(fixture_path('credentials', 'missing'))
        credentials = subject.credentials()

        assert credentials.email      is None
        assert credentials.password   is None
        assert credentials.user_token is None

    def test_credentials_are_blank_when_reading_empty_file(self):
        subject     = CredentialsFile(fixture_path('credentials', 'empty'))
        credentials = subject.credentials()

        assert credentials.email      is None
        assert credentials.password   is None
        assert credentials.user_token is None

    def test_credentials_are_blank_when_reading_empty_section(self):
        subject     = CredentialsFile(fixture_path('credentials', 'empty_section'))
        credentials = subject.credentials()

        assert credentials.email      is None
        assert credentials.password   is None
        assert credentials.user_token is None

    def test_credentials_set_when_reading_config(self):
        subject     = CredentialsFile(fixture_path('credentials', 'basic'))
        credentials = subject.credentials()

        assert credentials.email      == 'user@host.com'
        assert credentials.password   == 'password'
        assert credentials.user_token == 'token'

    def test_credentials_set_from_legacy_keys(self):
        subject     = CredentialsFile(fixture_path('credentials', 'legacy'))
        credentials = subject.credentials()

        assert credentials.email      == 'user@host.com'
        assert credentials.password   == 'password'
        assert credentials.user_token == 'token'
