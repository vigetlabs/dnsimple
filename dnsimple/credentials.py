import os.path

from ConfigParser import ConfigParser, NoSectionError, NoOptionError

from .exceptions import InvalidCredentialsException

class Credentials:
    """API credentials storage and validation"""
    def __init__(self, email = None, user_token = None, password = None):
        """
        Initialize credentials depending on type of authentication mode.

        Parameters
        ----------
        email: str
            Email address of account to use
        password: str
            Password to use for HTTP basic authentication
        user_token: str
            Token to use for token-based authentication
        """
        self.email        = email
        self.user_token   = user_token
        self.password     = password

    def is_blank(self):
        """
        Check if credentials have been supplied.

        Returns
        -------
        bool
            Were credentials supplied?
        """
        blank = True
        blank = blank and self.email      is None
        blank = blank and self.user_token is None
        blank = blank and self.password   is None

        return blank

    def is_valid(self):
        """
        Check if credentials are valid.  Requires caller to specify
        ``email`` along with ``password`` or ``user_token``

        Returns
        -------
        bool
            Are provided credentials valid?
        """
        valid = False
        valid = bool(self.email and self.user_token)
        valid = bool(self.email and self.password) if not valid else valid

        return valid

    def is_basic_auth(self):
        """
        Should HTTP basic authentication be used?

        Returns
        -------
        bool
            Authenticate with ``email`` / ``password``?
        """
        return self.is_valid() and bool(self.password)

    def is_token_auth(self):
        """
        Should token-based authentication be used?

        Returns
        -------
        bool
            Authenticate with ``email`` / ``user_token``?
        """
        return self.is_valid() and bool(self.user_token)

class CredentialsFile:
    """Represents a file that contains authentication credentials."""
    section = 'DNSimple'

    def __init__(self, path):
        """
        Initialize the reader with the path to a credentials file.

        Parameters
        ----------
        path: str
            Full path to a credentials configuration file
        """
        self.parser = ConfigParser()
        self.parser.read(path)

    def credentials(self):
        """
        Create a Credentials instance from the file contents.

        Returns
        -------
        Credentials
            A Credentials instance with the configured settings
        """
        return Credentials(
            self.__first(['email', 'username']),
            self.__first(['user_token', 'api_token']),
            self.__first(['password'])
        )

    def __first(self, keys):
        for key in keys:
            value = self.__get(key)

            if value:
                return value

    def __get(self, key):
        value = None

        try:
            value = self.parser.get(self.section, key)
        except (NoSectionError, NoOptionError):
            pass

        return value

class CredentialsSearch:
    """
    Search configured paths for a file containing authentication
    credentials.
    """
    def __init__(self, search_paths, filename):
        self.search_paths = search_paths
        self.filename     = filename

    def all(self):
        return [CredentialsFile(p).credentials() for p in self.__paths()]

    def first(self):
        for instance in self.all():
            return instance

    def __paths(self):
        return [path for path in self.__search_paths() if os.path.exists(path)]

    def __search_paths(self):
        return [self.__path_to_file(path) for path in self.search_paths]

    def __path_to_file(self, path):
        return os.path.expanduser(os.path.join(path, self.filename))
