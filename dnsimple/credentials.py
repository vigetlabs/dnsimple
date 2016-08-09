class InvalidCredentialsException(Exception):
    pass

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
