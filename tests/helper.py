from .context import dnsimple

import requests
import json

class TestHelper(object):

    def stub_response(self, data, success = True):
        raw_response = requests.Response()
        raw_response.json = lambda: data

        if success:
            raw_response.status_code = 200
        else:
            raw_response.status_code = 404

        response = dnsimple.response.Response(raw_response)

        return response

    def stub_request(self, subject, mocker, response, method = 'get'):
        request = mocker.stub()
        request.return_value = response

        request_instance = dnsimple.request.Request(dnsimple.credentials.Credentials())
        mocker.patch.object(request_instance, method, request)

        subject.request = lambda: request_instance

        return request
