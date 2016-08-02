import pytest

from .context import dnsimple

import requests

@pytest.fixture
def request():
    return dnsimple.request.Request(dnsimple.credentials.Credentials())

class RequestHelper:

    def stub_request(self, mocker, request, method_name, data = None, success = True):
        raw_response = requests.Response()
        raw_response.json = lambda: data

        response = dnsimple.response.Response(raw_response)
        response.was_successful = lambda: success

        method = mocker.stub()
        method.return_value = response

        mocker.patch.object(request, method_name, method)

        return method
