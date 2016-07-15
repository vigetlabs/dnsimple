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

