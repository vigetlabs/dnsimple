import os.path

from .credentials_file import CredentialsFile

class CredentialsSearch:
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
