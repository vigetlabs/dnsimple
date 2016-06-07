import json
import requests

from  requests.exceptions import RequestException

from .response import Response

class Request:

    sandbox = False

    def __init__(self, credentials):
        self.credentials     = credentials
        self.default_headers = {
            'Accept':       'application/json',
            'Content-Type': 'application/json'
        }

    def base_uri(self):
        host = 'api.dnsimple.com'

        if self.sandbox:
            host = 'api.sandbox.dnsimple.com'

        return 'https://{0}/v1/'.format(host)

    def request_uri(self, path):
        uri = self.base_uri() + path
        return uri

    def headers(self):
        headers = self.default_headers

        if self.credentials.is_token_auth():
            headers.update({'X-DNSimple-Token': self.credentials.email + ':' + self.credentials.user_token})

        return headers

    def basic_auth(self):
        auth = ()

        if self.credentials.is_basic_auth():
            auth = (self.credentials.email, self.credentials.password)

        return auth

    def get(self, endpoint):
        return self.__handle_request(lambda:
            requests.get(self.request_uri(endpoint),
                headers = self.headers(),
                auth    = self.basic_auth()
            )
        )

    def post(self, endpoint, data):
        return self.__handle_request(lambda:
            requests.post(self.request_uri(endpoint),
                headers = self.headers(),
                auth    = self.basic_auth(),
                data    = json.dumps(data)
            )
        )

    def delete(self, endpoint):
        return self.__handle_request(lambda:
            requests.delete(self.request_uri(endpoint),
                headers = self.headers(),
                auth    = self.basic_auth()
            )
        )

    def __handle_request(self, callback):
        try:
            return Response(callback())
        except requests.exceptions.RequestException:
            return Response(None)
