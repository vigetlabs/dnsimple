import pytest

import requests
from requests.exceptions import ConnectionError

from ..context import dnsimple

from dnsimple.connection  import Request
from dnsimple.credentials import Credentials
from dnsimple.exceptions  import UnauthorizedException

@pytest.fixture
def user_token_credentials():
    return Credentials(email = 'user@host.com', user_token = 'toke')

@pytest.fixture
def password_credentials():
    return Credentials(email = 'user@host.com', password = 'password')

@pytest.fixture
def domain_token_credentials():
    return Credentials(domain_token = 'token')

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

    def test_headers_returns_token_auth_headers_when_needed(self, user_token_credentials):
        subject = Request(user_token_credentials)

        assert subject.headers() == {
            'Accept':           'application/json',
            'Content-Type':     'application/json',
            'X-DNSimple-Token': 'user@host.com:toke'
        }

    def test_headers_returns_domain_token_auth_headers_when_needed(self, domain_token_credentials):
        subject = Request(domain_token_credentials)

        assert subject.headers() == {
            'Accept':                  'application/json',
            'Content-Type':            'application/json',
            'X-DNSimple-Domain-Token': 'token'
        }

    def test_headers_returns_no_auth_headers_when_using_password_auth(self, password_credentials):
        subject = Request(password_credentials)

        assert subject.headers() == {
            'Accept':           'application/json',
            'Content-Type':     'application/json'
        }

    def test_basic_auth_returns_empty_tuple_when_using_token_authentication(self, user_token_credentials):
        subject = Request(user_token_credentials)
        assert subject.basic_auth() == ()

    def test_basic_auth_returns_username_and_password_tuple_when_using_password_authentication(self, password_credentials):
        subject = Request(password_credentials)
        assert subject.basic_auth() == ('user@host.com', 'password')

    def test_get_returns_wrapped_response_on_success(self, user_token_credentials, mocker):
        subject  = Request(user_token_credentials)
        response = requests.models.Response()

        get = mocker.stub()
        get.return_value = response

        mocker.patch('requests.get', get)

        api_response = subject.get('domains')

        get.assert_called_once_with('https://api.dnsimple.com/v1/domains',
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-DNSimple-Token': 'user@host.com:toke'},
            auth    = (),
            params  = {}
        )

        assert isinstance(api_response, dnsimple.connection.Response)
        assert api_response.response == response

    def test_get_passes_params_to_request(self, user_token_credentials, mocker):
        subject = Request(user_token_credentials)
        get     = mocker.stub()

        mocker.patch('requests.get', get)

        api_response = subject.get('domains', {'key':'value'})

        get.assert_called_once_with('https://api.dnsimple.com/v1/domains',
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-DNSimple-Token': 'user@host.com:toke'},
            auth    = (),
            params  = {'key':'value'}
        )

    def test_get_returns_empty_response_on_failure(self, user_token_credentials, mocker):
        subject = Request(user_token_credentials)

        get = mocker.stub()
        get.side_effect = ConnectionError()

        mocker.patch('requests.get', get)

        api_response = subject.get('domains')

        assert isinstance(api_response, dnsimple.connection.Response)
        assert api_response.response is None

    def test_post_returns_wrapped_response_on_success(self, user_token_credentials, mocker):
        subject  = Request(user_token_credentials)
        response = requests.models.Response()

        post = mocker.stub()
        post.return_value = response

        mocker.patch('requests.post', post)

        api_response = subject.post('domains', {'key':'value'})

        post.assert_called_once_with('https://api.dnsimple.com/v1/domains',
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-DNSimple-Token': 'user@host.com:toke'},
            auth    = (),
            data    = '{"key": "value"}'
        )

        assert isinstance(api_response, dnsimple.connection.Response)
        assert api_response.response == response

    def test_post_returns_empty_response_on_failure(self, user_token_credentials, mocker):
        subject = Request(user_token_credentials)

        post = mocker.stub()
        post.side_effect = ConnectionError()

        mocker.patch('requests.post', post)

        api_response = subject.post('domains', {'key':'value'})

        assert isinstance(api_response, dnsimple.connection.Response)
        assert api_response.response is None

    def test_delete_returns_wrapped_response_on_success(self, user_token_credentials, mocker):
        subject  = Request(user_token_credentials)
        response = requests.models.Response()

        delete = mocker.stub()
        delete.return_value = response

        mocker.patch('requests.delete', delete)

        api_response = subject.delete('domains')

        delete.assert_called_once_with('https://api.dnsimple.com/v1/domains',
            headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'X-DNSimple-Token': 'user@host.com:toke'},
            auth    = ()
        )

        assert isinstance(api_response, dnsimple.connection.Response)
        assert api_response.response == response

    def test_delete_returns_empty_response_on_failure(self, user_token_credentials, mocker):
        subject = Request(user_token_credentials)

        delete = mocker.stub()
        delete.side_effect = ConnectionError()

        mocker.patch('requests.delete', delete)

        api_response = subject.delete('domains')

        assert isinstance(api_response, dnsimple.connection.Response)
        assert api_response.response is None

    def test_unauthorized_response_raises_exception(self, user_token_credentials, mocker):
        subject  = Request(user_token_credentials)
        response = requests.models.Response()

        response.status_code = 401

        get = mocker.stub()
        get.return_value = response

        mocker.patch('requests.get', get)

        with pytest.raises(UnauthorizedException) as exception:
            subject.get('domains')

        assert 'You are not authorized to access that resource' in str(exception.value)
