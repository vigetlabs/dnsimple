from requests.exceptions import ConnectionError

from ..context import dnsimple

from dnsimple.connection  import Request
from dnsimple.credentials import Credentials

import pytest

@pytest.fixture
def token_credentials():
    return Credentials(email = 'user@host.com', user_token = 'toke')

@pytest.fixture
def password_credentials():
    return Credentials(email = 'user@host.com', password = 'password')

@pytest.fixture
def subject():
    return Request(Credentials())

class TestRequest:
    def setup_method(self, method):
        Request.sandbox = False # default for class

    def test_base_uri_returns_production_uri_by_default(self, subject):
        assert subject.base_uri() == 'https://api.dnsimple.com/v1/'

    def test_base_uri_returns_sandbox_uri_when_requested(self, password_credentials):
        subject = Request(password_credentials, sandbox = True)
        assert subject.base_uri() == 'https://api.sandbox.dnsimple.com/v1/'

    def test_request_uri_creates_uri_from_path(self, subject):
        assert subject.request_uri('domains') == 'https://api.dnsimple.com/v1/domains'

    def test_headers_returns_token_auth_headers_when_needed(self, token_credentials):
        subject = Request(token_credentials)

        assert subject.headers() == {
            'Accept':           'application/json',
            'Content-Type':     'application/json',
            'X-DNSimple-Token': 'user@host.com:toke'
        }

    def test_headers_returns_no_auth_headers_when_using_password_auth(self, password_credentials):
        subject = Request(password_credentials)

        assert subject.headers() == {
            'Accept':           'application/json',
            'Content-Type':     'application/json'
        }

    def test_basic_auth_returns_empty_tuple_when_using_token_authentication(self, token_credentials):
        subject = Request(token_credentials)
        assert subject.basic_auth() == ()

    def test_basic_auth_returns_username_and_password_tuple_when_using_password_authentication(self, password_credentials):
        subject = Request(password_credentials)
        assert subject.basic_auth() == ('user@host.com', 'password')

    def test_get_returns_wrapped_response_on_success(self, token_credentials, mocker):
        subject = Request(token_credentials)

        get = mocker.stub()
        get.return_value = 'response'

        mocker.patch('requests.get', get)

        response = subject.get('domains')

        get.assert_called_once_with('https://api.dnsimple.com/v1/domains',
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-DNSimple-Token': 'user@host.com:toke'},
            auth    = (),
            params  = {}
        )

        assert isinstance(response, dnsimple.connection.Response)
        assert response.response == 'response'

    def test_get_passes_params_to_request(self, token_credentials, mocker):
        subject = Request(token_credentials)
        get     = mocker.stub()

        mocker.patch('requests.get', get)

        response = subject.get('domains', {'key':'value'})

        get.assert_called_once_with('https://api.dnsimple.com/v1/domains',
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-DNSimple-Token': 'user@host.com:toke'},
            auth    = (),
            params  = {'key':'value'}
        )

    def test_get_returns_empty_response_on_failure(self, token_credentials, mocker):
        subject = Request(token_credentials)

        get = mocker.stub()
        get.side_effect = ConnectionError()

        mocker.patch('requests.get', get)

        response = subject.get('domains')

        assert isinstance(response, dnsimple.connection.Response)
        assert response.response is None

    def test_post_returns_wrapped_response_on_success(self, token_credentials, mocker):
        subject = Request(token_credentials)

        post = mocker.stub()
        post.return_value = 'response'

        mocker.patch('requests.post', post)

        response = subject.post('domains', {'key':'value'})

        post.assert_called_once_with('https://api.dnsimple.com/v1/domains',
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-DNSimple-Token': 'user@host.com:toke'},
            auth    = (),
            data    = '{"key": "value"}'
        )

        assert isinstance(response, dnsimple.connection.Response)
        assert response.response == 'response'

    def test_post_returns_empty_response_on_failure(self, token_credentials, mocker):
        subject = Request(token_credentials)

        post = mocker.stub()
        post.side_effect = ConnectionError()

        mocker.patch('requests.post', post)

        response = subject.post('domains', {'key':'value'})

        assert isinstance(response, dnsimple.connection.Response)
        assert response.response is None

    def test_delete_returns_wrapped_response_on_success(self, token_credentials, mocker):
        subject = Request(token_credentials)

        delete = mocker.stub()
        delete.return_value = 'response'

        mocker.patch('requests.delete', delete)

        response = subject.delete('domains')

        delete.assert_called_once_with('https://api.dnsimple.com/v1/domains',
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-DNSimple-Token': 'user@host.com:toke'},
            auth    = ()
        )

        assert isinstance(response, dnsimple.connection.Response)
        assert response.response == 'response'

    def test_delete_returns_empty_response_on_failure(self, token_credentials, mocker):
        subject = Request(token_credentials)

        delete = mocker.stub()
        delete.side_effect = ConnectionError()

        mocker.patch('requests.delete', delete)

        response = subject.delete('domains')

        assert isinstance(response, dnsimple.connection.Response)
        assert response.response is None
