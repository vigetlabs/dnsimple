from .credentials        import InvalidCredentialsException, Credentials
from .credentials_search import CredentialsSearch
from .request            import Request
from .domain_collection  import DomainCollection
from .contact_collection import ContactCollection
from .search             import Search
from .registration       import Registration

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

    def contacts(self):
        return ContactCollection(self.request)

    def contact(self, id_or_email):
        return ContactCollection(self.request).find(id_or_email)

    def domain(self, name):
        return DomainCollection(self.request).find(name)

    def find(self, name):
        return Search(self.request).find(name)

    def check(self, name):
        return self.find(name).available

    def register(self, name, contact):
        return Registration(self.request).add(name, contact)
