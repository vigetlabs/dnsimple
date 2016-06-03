import json
import requests

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
        try:
            raw = requests.get(self.request_uri(endpoint), headers = self.headers(), auth=self.basic_auth())
            return Response(raw)
        except Exception:
            return Response(None)

    def post(self, endpoint, data):
        try:
            raw = requests.post(self.request_uri(endpoint),
                headers = self.headers(),
                auth    = self.basic_auth(),
                data    = json.dumps(data)
            )
            return Response(raw)
        except Exception:
            return Response(None)

    def delete(self, endpoint):
        try:
            raw = requests.delete(self.request_uri(endpoint), headers = self.headers(), auth = self.basic_auth())
            return Response(raw)
        except Exception:
            return Response(None)
