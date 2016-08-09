from .status import Status

class Search:
    """Find the registration status for a domain name."""
    def __init__(self, request):
        """
        Parameters
        ----------
        request: Request
            A Request instance to use when fetching API responses
        """
        self.request = request

    def find(self, name):
        """
        Find the registration status for the specified name.

        Parameters
        ----------
        name: str
            The domain name to query

        Returns
        -------
        Status
        """
        response = self.request.get('domains/{0}/check'.format(name))
        return Status(response.to_dict())
