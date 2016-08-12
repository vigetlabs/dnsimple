from . import *

@pytest.fixture
def domain(client):
    return client.domain('foo.com')

@pytest.fixture
def domain_from_token(domain):
    client = dnsimple.Client(domain_token = domain.token, sandbox = True)
    return client.domain(domain.name)

class TestRecords:

    def test_default_records(self, domain, domain_from_token):
        for d in [domain, domain_from_token]:
            # Test all to return list
            records = d.records().all()
            assert len(records) == 5

        counter = 0

        # Test iteration with __iter__
        for record in domain.records():
            counter += 1

        assert counter == 5

    def test_filtering_records(self, domain, domain_from_token):

        for d in [domain, domain_from_token]:
            # Filter to only 'NS' records
            assert [r.record_type for r in d.records(type = 'NS' )] == ['NS', 'NS', 'NS', 'NS']

            # Filter only 'SOA' records
            assert [r.record_type for r in d.records(type = 'SOA')] == ['SOA']

            # Filter only 'A' records
            assert [r             for r in d.records(type = 'A')  ] == []

    def test_creating_records(self, domain, domain_from_token):
        # Test creation without valid attributes
        success = domain.records().add({})
        assert not success

        # Create A records
        a = domain.records().add({'name': '', 'record_type': 'A', 'content': '192.168.1.1'})
        assert a

        subdomain = domain.records().add({'name': 'subdomain', 'record_type': 'A', 'content': '192.168.1.2'})
        assert subdomain

        # Create a CNAME record
        cname = domain.records().add({'name':'www', 'record_type': 'CNAME', 'content': domain.name})
        assert cname

        # Create from token-authed domain
        record = domain_from_token.records().add({'name':'domain-token', 'record_type': 'A', 'content': '192.168.1.3'})
        assert record

    def test_updating_records(self, domain, domain_from_token):
        for d in [domain, domain_from_token]:
            record = d.records().add({'name': 'old', 'record_type': 'A', 'content': '192.168.1.3'})
            assert record

            assert record.update({'name': 'new'})

            record = d.record('new')
            assert record

            # Empty update should fail
            assert not record.update({})

            record.delete()

    def test_finding_records(self, domain, domain_from_token):
        for d in [domain, domain_from_token]:
            # Ensure created records can be retrieved
            assert [r.name for r in d.records(type = 'A')    ] == ['', 'domain-token', 'subdomain']
            assert [r.name for r in d.records(type = 'CNAME')] == ['www']

            # Filter based on name and type
            assert [r.content for r in d.records(type = 'A', name = '')] == ['192.168.1.1']

            # Test find with multiple results
            with pytest.raises(dnsimple.collections.MultipleResultsException) as ex:
                d.record('')

            assert 'Multiple results returned for query' in str(ex.value)

            # Find by name
            www    = d.record('www')
            www_id = www.id

            assert www.name        == 'www'
            assert www.record_type == 'CNAME'

            # Find by ID
            www = d.record(www_id)

            assert www.name == 'www'

    def test_destroying_records(self, domain, domain_from_token):
        # Delete user-created A records
        record = domain.record('', type = 'A')
        assert record.delete()

        record = domain_from_token.record('domain-token')
        assert record.delete()

        # Delete CNAME record
        assert domain.record('www').delete()

        # Ensure system record can't be deleted
        assert not domain.record('', type = 'SOA').delete()
        assert not domain_from_token.record('', type = 'SOA').delete()
