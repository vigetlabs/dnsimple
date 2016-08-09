from . import *

@pytest.fixture
def domain(client):
    return client.domain('foo.com')

class TestRecords:

    def test_default_records(self, domain):
        # Test all to return list
        records = domain.records().all()
        assert len(records) == 5

        counter = 0

        # Test iteration with __iter__
        for record in domain.records():
            counter += 1

        assert counter == 5

    def test_filtering_records(self, domain):
        # Filter to only 'NS' records
        assert [r.record_type for r in domain.records(type = 'NS' )] == ['NS', 'NS', 'NS', 'NS']

        # Filter only 'SOA' records
        assert [r.record_type for r in domain.records(type = 'SOA')] == ['SOA']

        # Filter only 'A' records
        assert [r             for r in domain.records(type = 'A')  ] == []

    def test_creating_records(self, domain):
        # Test creation without valid attributes
        failure = domain.records().add({})
        assert not failure

        # Create A records
        a = domain.records().add({'name': '', 'record_type': 'A', 'content': '192.168.1.1'})
        assert a

        subdomain = domain.records().add({'name': 'subdomain', 'record_type': 'A', 'content': '192.168.1.2'})
        assert subdomain

        # Create a CNAME record
        cname = domain.records().add({'name':'www', 'record_type': 'CNAME', 'content': domain.name})
        assert cname

    def test_updating_records(self, domain):
        record = domain.records().add({'name': 'old', 'record_type': 'A', 'content': '192.168.1.3'})
        assert record

        assert record.update({'name': 'new'})

        record = domain.record('new')
        assert record

        # Empty update should fail
        assert not record.update({})

        record.delete()

    def test_finding_records(self, domain):
        # Ensure created records can be retrieved
        assert [r.name for r in domain.records(type = 'A')    ] == ['', 'subdomain']
        assert [r.name for r in domain.records(type = 'CNAME')] == ['www']

        # Filter based on name and type
        assert [r.content for r in domain.records(type = 'A', name = '')] == ['192.168.1.1']

        # Test find with multiple results
        with pytest.raises(dnsimple.collections.MultipleResultsException) as ex:
            domain.record('')

        assert 'Multiple results returned for query' in str(ex.value)

        # Find by name
        www    = domain.record('www')
        www_id = www.id

        assert www.name        == 'www'
        assert www.record_type == 'CNAME'

        # Find by ID
        www = domain.record(www_id)

        assert www.name == 'www'

    def test_destroying_records(self, domain):
        # Delete user-created A records
        for record in domain.records(type = 'A'):
            assert record.delete()

        # Delete CNAME record
        assert domain.record('www').delete()

        # Ensure system record can't be deleted
        assert not domain.record('', type = 'SOA').delete()
