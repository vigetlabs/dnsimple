from .credentials import InvalidCredentialsException, Credentials
from .request import Request
from .domain_collection import DomainCollection

class Client:

    def __init__(self, sandbox = False, email = None, user_token = None, password = None):
        self.credentials = Credentials(email, user_token, password)

        if not self.credentials.is_valid():
            raise InvalidCredentialsException("Invalid credentials supplied")

        Request.sandbox = sandbox

    def domains(self):
        return DomainCollection(self.credentials)
