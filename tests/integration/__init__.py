import os.path
import uuid

import pytest

from ..context import dnsimple

@pytest.fixture
def client():
    return dnsimple.Client(
        sandbox                  = True,
        credentials_search_paths = [os.path.dirname(__file__)]
    )

unregistered_domain_name = 'example-{0}.com'.format(uuid.uuid4())

# Ensure no domains exist
for domain in client().domains():
    domain.delete()

# Ensure no contacts exist
for contact in client().contacts():
    contact.delete()
