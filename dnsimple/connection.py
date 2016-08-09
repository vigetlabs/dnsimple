import json
import requests

from requests.exceptions import RequestException

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

class Response:
    """Wrap a response from the DNSimple API"""

    def __init__(self, response = None):
        """
        Parameters
        ----------
        response: requests.models.Response or None
            A response object or None if no response
        """
        self.response = response

    def was_successful(self):
        """
        Determines if the request was successful based on the HTTP status
        code.  Anything between 200 and 299 is successful

        Returns
        -------
        bool
        """
        return (
            self.response is not None and
            self.response.status_code in range(200, 300)
        )

    def error(self):
        """
        The error message from the response if available.

        Returns
        -------
        message: str or None
            The message string or ``None`` if no errors
        """
        return self.to_dict('message')

    def to_dict(self, key = None, default = None):
        """
        The dictionary representation of the decoded response. Has the
        ability to fetch the value of a specific top-level key and return
        a default value if the key does not exist.

        Parameters
        ----------
        key: str or None
            The key to fetch, or None to fetch the full dict
        default
            The value to return when the key is not found

        Returns
        -------
        value
            The data type varies depending on the source data, key, and
            the type of the default parameter
        """
        data = {}

        try:
            data = self.response.json()
        except AttributeError:
            pass

        return data.get(key, default) if key else data
