class Response:

    def __init__(self, response = None):
        self.response = response

    def was_successful(self):
        return self.response is not None and self.response.status_code in [200, 201]

    def to_dict(self):
        data = dict()

        if self.was_successful():
            data = self.response.json()

        return data
