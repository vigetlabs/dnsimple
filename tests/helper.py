from .context import dnsimple

class TestHelper(object):

    def stub_response(self, data, success = True):
        response = dnsimple.response.Response()
        response.was_successful = lambda: success
        response.to_dict        = lambda: data

        return response

    def stub_request(self, subject, mocker, response, method = 'get'):
        request = mocker.stub()
        request.return_value = response

        request_instance = dnsimple.request.Request(dnsimple.credentials.Credentials())
        mocker.patch.object(request_instance, method, request)

        subject.request = lambda: request_instance

        return request
