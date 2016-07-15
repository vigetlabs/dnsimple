import os.path

import pytest

from ..context import dnsimple

@pytest.fixture
def client():
    return dnsimple.Client(
        sandbox                  = True,
        credentials_search_paths = [os.path.dirname(__file__)]
    )

# Ensure no domains exist
for domain in client().domains():
    domain.delete()
