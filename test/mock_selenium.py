""" Mock a selenium driver object """
import os
import textwrap
import time
from lxml import html


class MockWebDriverWait:
    """ Mock WebDriverWait """

    def __init__(self, driver, timeout, wait_time=0.1):
        self._driver = driver
        self._timeout = timeout
        self._wait_time = wait_time

    def until(self, message=""):
        """ until """
        if self._wait_time < self._timeout:
            time.sleep(self._wait_time)
        else:
            raise TimeoutError(message)


class MockWebElement:
    """ Mock a selenium web element """

    def __init__(self, element=None):
        self.element = element

    def click(self):
        """ click """
        class_value = self.element.classes._get_class_value()
        if class_value:
            return True
        raise ValueError

    def send_keys(self, keys):
        # pylint: disable=unused-argument
        """ send keys """
        if isinstance(self.element, html.InputElement):
            return True
        raise TypeError

    @property
    def text(self):
        """ text """
        elem_str = str(self.element.text_content())
        elem_str = textwrap.dedent(elem_str)
        elem_str = os.linesep.join([s for s in elem_str.splitlines() if s])
        return elem_str


class MockWebDriver:
    """ Mock a selenium web driver """

    def __init__(self, options=None):
        self.options = options
        self._content = None
        self.url = None

    def __repr__(self):
        return f"<{self.__class__.__name__}>"

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        self.quit()

    def quit(self):
        """ quit """

    @property
    def current_url(self):
        """ current url """
        return

    def find_element_by_xpath(self, xpath):
        """ find element by xpath """
        tree = html.fromstring(self._content)
        res = tree.xpath(xpath)
        return MockWebElement(element=res[0])

    def get(self, url):
        """ get """
        self.url = url
        with open(url) as file:
            content = file.read()
        self._content = content
        return content

    def back(self):
        """ back """

    def get_cookies(self):
        # pylint: disable=no-self-use
        """ get cookies """
        return [
            {"name": "PHPSESSID", "value": "00000"},
            {"name": "UID", "value": "11111"},
        ]
