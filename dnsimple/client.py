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
        credentials = Credentials(email, user_token, password)

        if credentials.is_blank():
            credentials = CredentialsSearch(credentials_search_paths, credentials_filename).first()

        if credentials is None or not credentials.is_valid():
            raise InvalidCredentialsException("Invalid credentials supplied")

        self.request = Request(credentials, sandbox)

    def domains(self):
        return DomainCollection(self.request)

    def domain(self, name):
        return DomainCollection(self.request).find(name)
