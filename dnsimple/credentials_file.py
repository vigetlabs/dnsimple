from ConfigParser import ConfigParser, NoSectionError, NoOptionError

from .credentials import Credentials

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

