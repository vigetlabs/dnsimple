from ..context import dnsimple

from dnsimple.status import Status

class TestStatus:
    def test_assign_assigns_attributes(self):
        subject = Status()
        subject.assign({'available':False})

        assert subject.available == False
