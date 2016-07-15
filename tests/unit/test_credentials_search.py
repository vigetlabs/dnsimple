from ..context import dnsimple, fixture_path

from dnsimple.credentials import Credentials
from dnsimple.credentials_search import CredentialsSearch

class TestCredentialsSearch:

    def test_all_is_empty_when_no_files_found(self):
        subject = CredentialsSearch([fixture_path('credentials')], 'missing')
        assert subject.all() == []

    def test_first_is_none_when_no_files_found(self):
        subject = CredentialsSearch([fixture_path('credentials')], 'missing')
        assert subject.first() is None

    def test_all_returns_single_credentials(self):
        subject = CredentialsSearch([fixture_path('credentials')], 'basic')
        all     = subject.all()

        assert len(all) == 1

        credentials = all[0]

        assert isinstance(credentials, Credentials)

        assert credentials.email      == 'user@host.com'
        assert credentials.user_token == 'token'
        assert credentials.password   == 'password'

    def test_first_returns_first_match_when_only_one(self):
        subject     = CredentialsSearch([fixture_path('credentials')], 'basic')
        credentials = subject.first()

        assert isinstance(credentials, Credentials)
        assert credentials.email == 'user@host.com'
        assert credentials.user_token == 'token'
        assert credentials.password   == 'password'

    def test_all_returns_multiple_matches(self):
        paths   = [fixture_path('credentials', '1'), fixture_path('credentials', '2')]
        subject = CredentialsSearch(paths, 'credentials')
        all     = subject.all()

        assert len(all) == 2

        assert all[0].email == 'user1@host.com'
        assert all[1].email == 'user2@host.com'

    def test_first_returns_first_match_when_multiple(self):
        paths       = [fixture_path('credentials', '1'), fixture_path('credentials', '2')]
        subject     = CredentialsSearch(paths, 'credentials')
        credentials = subject.first()

        assert isinstance(credentials, Credentials)
        assert credentials.email == 'user1@host.com'

    def test_all_returns_matches_in_order(self):
        paths   = [fixture_path('credentials', '2'), fixture_path('credentials', '1')]
        subject = CredentialsSearch(paths, 'credentials')
        all     = subject.all()

        assert all[0].email == 'user2@host.com'
        assert all[1].email == 'user1@host.com'

    def test_first_returns_first_match_when_alternate_search_order(self):
        paths       = [fixture_path('credentials', '2'), fixture_path('credentials', '1')]
        subject     = CredentialsSearch(paths, 'credentials')
        credentials = subject.first()

        assert isinstance(credentials, Credentials)
        assert credentials.email == 'user2@host.com'
