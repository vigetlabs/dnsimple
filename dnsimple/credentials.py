class InvalidCredentialsException(Exception):
    pass

class Credentials:
    def __init__(self, email = None, user_token = None, password = None):
        self.email        = email
        self.user_token   = user_token
        self.password     = password

    def is_valid(self):
        valid = False
        valid = bool(self.email and self.user_token)
        valid = bool(self.email and self.password) if not valid else valid

        return valid

    def is_basic_auth(self):
        return self.is_valid() and bool(self.password)

    def is_token_auth(self):
        return self.is_valid() and bool(self.user_token)
