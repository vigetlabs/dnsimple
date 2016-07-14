from ConfigParser import ConfigParser, NoSectionError, NoOptionError

from .credentials import Credentials

class CredentialsFile:

    section = 'DNSimple'

    def __init__(self, path):
        self.parser = ConfigParser()
        self.parser.read(path)

    def credentials(self):
        return Credentials(
            self.first(['email', 'username']),
            self.first(['user_token', 'api_token']),
            self.first(['password'])
        )

    def first(self, keys):
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

