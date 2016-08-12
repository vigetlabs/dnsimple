from . import *

class TestDomains:

    def test_domain_list_empty(self, client):
        # Test returning as a list
        assert client.domains().all() == []

        counter = 0

        # Test iteration with `__iter__`
        for domain in client.domains():
            counter += 1

        assert counter == 0

    def test_domain_creation(self, client):
        # Test creating without valid attributes
        failure = client.domains().add({})
        assert not failure

        names = ['foo.com', 'bar.com']

        # Test creation
        for name in names:
            domain = client.domains().add({'name': name})
            assert domain
            assert domain.name == name

        assert [d.name for d in client.domains()] == names

    def test_domain_token_authentication(self, client):
        allowed_domain = client.domain('foo.com')
        assert allowed_domain

        client = dnsimple.Client(domain_token = allowed_domain.token, sandbox = True)

        with pytest.raises(dnsimple.exceptions.UnauthorizedException) as exception:
            client.domains().all()

        assert "You are not authorized to access that resource" in str(exception.value)

        # Requests for the domain return the domain record
        assert client.domain('foo.com')     == allowed_domain

        # Requests for another registered domain return the domain to which the token
        # is associated
        assert client.domain('bar.com') == allowed_domain

        # Requests for any domain (hitting the /v1/domains/:domain endpoint) return
        # the domain to which the token is associated
        assert client.domain('missing.com') == allowed_domain
