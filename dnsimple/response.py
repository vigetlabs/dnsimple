class Response:

    def __init__(self, response = None):
        self.response = response

    def was_successful(self):
        return self.response is not None and self.response.status_code in [200, 201]

    def error(self):
        return self.to_dict('message')

    def to_dict(self, key = None, default = None):
        data = {}

        try:
            data = self.response.json()
        except AttributeError:
            pass

        return data.get(key, default) if key else data
