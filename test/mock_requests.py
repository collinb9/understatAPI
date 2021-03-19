""" Mock the requests library """
from requests.exceptions import HTTPError


class MockResponse:
    """ Mock response from requests.get() """

    def __init__(self, url, status_code=200, reason="OK"):
        self.url = url
        self.status_code = status_code
        self.reason = reason
        self.url = url

    @property
    def content(self):
        """ Response.content """
        with open(self.url) as file:
            content = file.read()
        return content

    @property
    def text(self):
        """ Response.content """
        with open(self.url) as file:
            text = file.read()
        return text

    def raise_for_status(self):
        """Raises `HTTPError`, if one occurred."""

        http_error_msg = ""
        reason = self.reason
        if 400 <= self.status_code < 500:
            http_error_msg = u"%s Client Error: %s for url: %s" % (
                self.status_code,
                reason,
                self.url,
            )

        elif 500 <= self.status_code < 600:
            http_error_msg = u"%s Server Error: %s for url: %s" % (
                self.status_code,
                reason,
                self.url,
            )

        if http_error_msg:
            raise HTTPError(http_error_msg, response=self)


def mocked_requests_get(*args, **kwargs):
    """
    Return a MockResponse object
    """
    return MockResponse(*args, **kwargs)
