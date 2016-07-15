from .credentials        import InvalidCredentialsException, Credentials
from .credentials_search import CredentialsSearch
from .request            import Request
from .domain_collection  import DomainCollection

class Client:

    def __init__(self,
        sandbox                  = False,
        email                    = None,
        user_token               = None,
        password                 = None,
        credentials_search_paths = ['.', '~'],
        credentials_filename     = '.dnsimple'
    ):
        self.credentials = Credentials(email, user_token, password)

        if self.credentials.is_blank():
            self.credentials = CredentialsSearch(credentials_search_paths, credentials_filename).first()

        if self.credentials is None or not self.credentials.is_valid():
            raise InvalidCredentialsException("Invalid credentials supplied")

        Request.sandbox = sandbox

    def domains(self):
        return DomainCollection(self.credentials)

    def domain(self, name):
        return DomainCollection(self.credentials).find(name)
