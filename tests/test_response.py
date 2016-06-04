import requests.models

from .context import dnsimple

from dnsimple.response import Response

class TestResponse:
    def test_was_successful_is_false_when_there_is_no_response(self):
        subject = Response(None)
        assert subject.was_successful() is False

    def test_was_successful_is_false_when_response_is_not_successful(self):
        response = requests.models.Response()
        response.status_code = 500

        subject  = Response(response)

        assert subject.was_successful() is False

    def test_was_successful_is_true_when_response_is_successful(self):
        response = requests.models.Response()
        response.status_code = 200

        subject = Response(response)

        assert subject.was_successful() is True

    def test_to_dict_is_empty_when_no_response(self):
        subject = Response(None)
        assert subject.to_dict() =={}

    def test_to_dict_returns_decoded_data(self, monkeypatch):
        response = requests.models.Response()
        response.status_code = 200

        monkeypatch.setattr(response, 'json', lambda: {'key':'value'})

        subject = Response(response)

        assert subject.to_dict() == {'key':'value'}
