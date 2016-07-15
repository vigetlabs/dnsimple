import requests.models

from ..context import dnsimple

from dnsimple.response import Response

class TestResponse:
    def stub_response(self, status = 200, data = {}):
        response = requests.models.Response()
        response.status_code = status
        response.json        = lambda: data

        return response

    def test_was_successful_is_false_when_there_is_no_response(self):
        subject = Response(None)
        assert subject.was_successful() is False

    def test_was_successful_is_false_when_response_is_not_successful(self):
        subject  = Response(self.stub_response(status = 500))
        assert subject.was_successful() is False

    def test_was_successful_is_true_when_response_is_successful(self):
        subject = Response(self.stub_response())
        assert subject.was_successful() is True

    def test_error_is_none_by_default(self):
        subject = Response(None)
        assert subject.error() is None

    def test_error_returns_error_message(self):
        subject = Response(self.stub_response(data = {'message': 'domain `foo.com` not found'}))
        assert subject.error() == 'domain `foo.com` not found'

    def test_to_dict_is_empty_when_no_response(self):
        subject = Response(None)
        assert subject.to_dict() =={}

    def test_to_dict_returns_decoded_data(self, monkeypatch):
        subject = Response(self.stub_response(data = {'key':'value'}))

        assert subject.to_dict() == {'key':'value'}

    def test_to_dict_returns_data_at_specified_key(self):
        subject = Response(self.stub_response(data = {'key':'value'}))
        assert subject.to_dict('key') == 'value'

    def test_to_dict_returns_none_for_missing_key(self):
        subject = Response(self.stub_response(data = {}))
        assert subject.to_dict('key') is None

    def test_to_dict_returns_user_specified_default_for_missing_key(self):
        subject = Response(self.stub_response(data = {}))
        assert subject.to_dict('key', 'missing') == 'missing'
