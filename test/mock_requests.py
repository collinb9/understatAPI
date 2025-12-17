"""Mock the requests library"""

import json
from requests.exceptions import HTTPError


class MockResponse:
    """Mock response from requests.get()"""

    def __init__(self, url=None, status_code=200, reason="OK", **kwargs):
        # Accept and ignore extra kwargs like 'headers' that requests.get() accepts
        self.url = url
        self.status_code = status_code
        self.reason = reason

    @property
    def content(self):
        """Response.content"""
        with open(self.url) as file:
            content = file.read()
        return content

    @property
    def text(self):
        """Response.content"""
        with open(self.url) as file:
            text = file.read()
        return text

    def json(self):
        """Response.json()"""
        with open(self.url) as file:
            return json.load(file)

    def raise_for_status(self):
        """Raises ``HTTPError``, if one occurred."""

        http_error_msg = ""
        reason = self.reason
        if 400 <= self.status_code < 500:
            http_error_msg = "%s Client Error: %s for url: %s" % (
                self.status_code,
                reason,
                self.url,
            )

        elif 500 <= self.status_code < 600:
            http_error_msg = "%s Server Error: %s for url: %s" % (
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
