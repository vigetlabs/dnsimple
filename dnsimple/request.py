import json
import requests

from  requests.exceptions import RequestException

from .response import Response

class Request:
    """Send authenticated requests to the DNSimple API."""

    def __init__(self, credentials, sandbox = False):
        """
        Parameters
        ----------
        credentials: Credentials
            User credentials for making authenticated requests
        sandbox: boolean
            Whether or not to use the sandbox API endpoint
        """
        self.credentials     = credentials
        self.sandbox         = sandbox
        self.default_headers = {
            'Accept':       'application/json',
            'Content-Type': 'application/json'
        }

    def get(self, path, params = {}):
        """
        Perform an HTTP GET request.

        Parameters
        ----------
        path: str
            Path to the desired resource
        params: dict
            Optional parameters to pass to the request

        Returns
        -------
        Response
        """
        return self.__handle_request(lambda:
            requests.get(self.request_uri(path),
                headers = self.headers(),
                auth    = self.basic_auth(),
                params  = params
            )
        )

    def post(self, path, data):
        """
        Perform an HTTP POST request.

        Parameters
        ----------
        path: str
            Path to the desired resource
        data: dict
            Parameters to pass to the request

        Returns
        -------
        Response
        """
        return self.__handle_request(lambda:
            requests.post(self.request_uri(path),
                headers = self.headers(),
                auth    = self.basic_auth(),
                data    = json.dumps(data)
            )
        )

    def put(self, path, data):
        """
        Perform an HTTP PUT request.

        Parameters
        ----------
        path: str
            Path to the desired resource
        data: dict
            Parameters to pass to the request

        Returns
        -------
        Response
        """
        return self.__handle_request(lambda:
            requests.put(self.request_uri(path),
                headers = self.headers(),
                auth    = self.basic_auth(),
                data    = json.dumps(data)
            )
        )

    def delete(self, path):
        """
        Perform an HTTP DELETE request.

        Parameters
        ----------
        path: str
            Path to the desired resource

        Returns
        -------
        Response
        """
        return self.__handle_request(lambda:
            requests.delete(self.request_uri(path),
                headers = self.headers(),
                auth    = self.basic_auth()
            )
        )

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

    def __handle_request(self, callback):
        try:
            return Response(callback())
        except requests.exceptions.RequestException:
            return Response(None)
