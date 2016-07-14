import os
import sys

sys.path.insert(0, os.path.abspath('..'))

import dnsimple

def fixture_path(*paths):
    return os.path.join(os.path.dirname(__file__), 'fixtures', *paths)
