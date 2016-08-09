from .credentials        import InvalidCredentialsException, Credentials
from .credentials_search import CredentialsSearch
from .request            import Request
from .domain_collection  import DomainCollection
from .contact_collection import ContactCollection
from .search             import Search
from .registration       import Registration

class Client:
    """The main entry point for interacting with the DNSimple API."""
    def __init__(self,
        sandbox                  = False,
        email                    = None,
        user_token               = None,
        password                 = None,
        credentials_search_paths = ['.', '~'],
        credentials_filename     = '.dnsimple'
    ):
        """
        Create an authenticated API client.  Supports multiple authentication
        methods.

        For user token authentication, supply ``email`` and ``user_token``.
        For HTTP basic authentication, supply ``email`` and ``password``.

        If no credentials are provided to the constructor, the configured
        ``credentials_search_paths`` will be searched for a credentials file
        named ``credentials_filename``.  This file must be in the format:

            [DNSimple]
            email: user@host.com
            password: password

        You can use either HTTP Basic or user token authentication credentials
        in this file.

        Parameters
        ----------
        sandbox: bool
            Should the client authenticate against the Sandbox API?
        email: str
            Email address for the account
        user_token: str
            Token for the user specified by ``email``
        password: str
            Password for the user (if using HTTP basic auth)
        credentials_search_paths: list of str
            The paths to search for credentials files, will perform user
            expansion if the path contains ``~```
        credentials_filename: str
            The filename that will be used for credentials (first match)

        Raises
        ------
        InvalidCredentialsException
            If no credentials are supplied or if a credentials file isn't
            found in the specified search path(s)
        """
        credentials = Credentials(email, user_token, password)

        if credentials.is_blank():
            credentials = CredentialsSearch(credentials_search_paths, credentials_filename).first()

        if credentials is None or not credentials.is_valid():
            raise InvalidCredentialsException("Invalid credentials supplied")

        self.request = Request(credentials, sandbox)

    def domains(self):
        """
        Fetch a list of domains associated with the current account.

        Returns
        -------
        DomainCollection
        """
        return DomainCollection(self.request)

    def domain(self, id_or_name):
        """
        Find a single domain by ID or name for the current account.

        Parameters
        ----------
        id_or_name: int or str
            The ID or name of the domain to find

        Returns
        -------
        domain: Domain or None
            Domain instance if found, otherwise ``None``
        """
        return DomainCollection(self.request).find(id_or_name)

    def contacts(self):
        """
        Fetch a list of contacts associated with the current account.

        Returns
        -------
        ContactCollection
        """
        return ContactCollection(self.request)

    def contact(self, id_or_email):
        """
        Find a single domain by ID or email for the current account.

        Parameters
        ----------
        id_or_email: int or str
            The ID or email address for the contact to find

        Returns
        -------
        contact: Contact or None
            Contact instance if found, otherwise ``None``
        """
        return ContactCollection(self.request).find(id_or_email)

    def find(self, name):
        """
        Find an existing domain registration.

        Parameters
        ----------
        name: str
            The domain name to check

        Returns
        -------
        Status
            The status of the domain registration
        """
        return Search(self.request).find(name)

    def check(self, name):
        """
        Quick check of a domain registration to see if it's available.

        Parameters
        ----------
        name: str
            The domain name to check

        Returns
        -------
        bool
            Whether the domain name is available for registration
        """
        return self.find(name).available

    def register(self, name, contact):
        """
        Register a domain name and associate it with a contact.

        Parameters
        ----------
        name: str
            The name of the domain to register, must be available
        contact: Contact
            A Contact instance associated with your account

        Returns
        -------
        domain: Domain or None
            Domain instance if successfully registered, otherwise ``None``
        """
        return Registration(self.request).add(name, contact)

    def transfer(self, name, contact):
        """
        Transfer a domain from another registrar into DNSimple.

        Parameters
        ----------
        name: str
            The name of the domain to transfer
        contact: Contact
            The contact who will hold the domain registration

        Returns
        -------
        bool
            Was the domain transfer successful?
        """
        response = self.request.post('domain_transfers', {
            'domain': {'name': name, 'registrant_id': contact.id}
        })

        return response.was_successful()
