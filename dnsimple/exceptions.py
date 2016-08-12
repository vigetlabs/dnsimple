class InvalidCredentialsException(Exception):
    """Credentials do not have the required authentication information"""
    pass

class UnauthorizedException(Exception):
    """Request for resource is unauthorized"""
    pass

class MultipleResultsException(Exception):
    """Multiple results returned for a response that expected one"""
    pass
