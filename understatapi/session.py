"""Session objects other than the default requests.Session"""
import abc


class Session(abc.ABC):
    """
    An abstract class which defines the interface for a session object

    This is designed to be compatible with the interface used by
    the ``requests.Session`` object
    """

    @abc.abstractmethod
    def close(self) -> None:
        """Close the session"""
        ...


class Response(abc.ABC):
    """
    An abstract class which defines the interface for the response to a
    request made through a :py:class:`~understatapi.session.Session`
    """

    def __init__(self, url, status_code=200, reason="OK"):
        self.url = url
        self.status_code = status_code
        self.reason = reason
        self.url = url

    @abc.abstractproperty
    def content(self) -> str:
        """ Response.content """
        with open(self.url) as file:
            content = file.read()
        return content

    @abc.abstractproperty
    def text(self) -> str:
        """ Response.content """
        with open(self.url) as file:
            text = file.read()
        return text

    def raise_for_status(self) -> None:
        """
        A method which is necessary to integrate with the API. Typically
        there will be no need to override this method
        """
        ...


class LocalSession(Session):
    """
    Read local html files instead of making http requests
    """

    def close(self) -> None:
        print("Closing ...")