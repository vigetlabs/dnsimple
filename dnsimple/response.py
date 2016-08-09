class Response:
    """Wrap a response from the DNSimple API"""

    def __init__(self, response = None):
        """
        Parameters
        ----------
        response: requests.models.Response or None
            A response object or None if no response
        """
        self.response = response

    def was_successful(self):
        """
        Determines if the request was successful based on the HTTP status
        code.  Anything between 200 and 299 is successful

        Returns
        -------
        bool
        """
        return (
            self.response is not None and
            self.response.status_code in range(200, 300)
        )

    def error(self):
        """
        The error message from the response if available.

        Returns
        -------
        message: str or None
            The message string or ``None`` if no errors
        """
        return self.to_dict('message')

    def to_dict(self, key = None, default = None):
        """
        The dictionary representation of the decoded response. Has the
        ability to fetch the value of a specific top-level key and return
        a default value if the key does not exist.

        Parameters
        ----------
        key: str or None
            The key to fetch, or None to fetch the full dict
        default
            The value to return when the key is not found

        Returns
        -------
        value
            The data type varies depending on the source data, key, and
            the type of the default parameter
        """
        data = {}

        try:
            data = self.response.json()
        except AttributeError:
            pass

        return data.get(key, default) if key else data
