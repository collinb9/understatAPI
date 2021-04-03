""" Use the search bar of understat.com """
from types import TracebackType
from typing import Tuple, Sequence, Iterator
import requests
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Search:
    """
    Use the search bar on understat.com

    All results matching the given player name will be returned
    """

    opts = Options()
    opts.set_headless()
    url = "https://understat.com/"

    def __init__(
        self,
        player_name: str,
        session: requests.Session,
        max_ids: int = 5,
        page_load_timeout: int = 5,
    ) -> None:
        """
        :player_name: str: Name of player to search for
        :session: requests.Session: A requests `Session` object
        :max_ids: int: The maximum number of player ids to return
        :page_load_timeout: int: Number of seconds to wait for the page
            to load before raising a `TimeoutError`
        """
        self.player_name = player_name
        self.session = session
        self.max_ids = max_ids
        self.page_load_timeout = page_load_timeout
        self._initialise_browser()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __enter__(self) -> "Search":
        return self

    def __exit__(
        self,
        exception_type: type,
        exception_value: BaseException,
        traceback: TracebackType,
    ) -> None:
        cookies = self.browser.get_cookies()
        for cookie in cookies:
            self.session.cookies.set(cookie["name"], cookie["value"])
        self.browser.quit()

    def _initialise_browser(self) -> None:
        """ Inilise the WebDriver object """
        self.browser = Firefox(options=self.opts)

    def get_player_ids(self) -> Iterator[str]:
        """
        Get the ids that are returned when you search for the given
        player name
        """
        self.browser.get(self.url)
        self._make_search()
        players = self._get_search_results()
        for i, player_id in enumerate(self._cycle_results(players)):
            yield player_id
            if i >= self.max_ids - 1:
                break

    @staticmethod
    def _get_player_id_from_url(url: str) -> str:
        """
        Get the player id from a url
        """
        id_number = url.split("/")[-1]
        return id_number

    def _cycle_results(
        self, results: Sequence[Tuple[str, str]]
    ) -> Iterator[str]:
        """
        Cycles through each of the search results, getting the url each time
        """
        for i, _ in enumerate(results):
            self.browser.find_element_by_xpath(
                f"//*[@id='header']/div/nav[2]/ul/"
                f"li[1]/span[1]/div/div/div[{i+1}]"
            ).click()
            player_id = self._get_player_id_from_url(self.browser.current_url)
            self.browser.back()
            self._make_search()
            yield player_id

    def _wait_for_page_load(self, **kwargs: int) -> None:
        """ Wait for the page loading screen to disappear """
        try:
            WebDriverWait(
                self.browser, self.page_load_timeout, **kwargs
            ).until(
                EC.invisibility_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[1]")
                )
            )
        except TimeoutError as err:
            raise TimeoutError(err) from err

    def _make_search(self, **kwargs: int) -> None:
        """
        Make the search
        """
        # Wait for loading page to disappear
        self._wait_for_page_load()
        # Open the search bar
        player_search = self.browser.find_element_by_xpath(
            "//*[@id='header']/div/nav[2]/ul/li[1]"
        )
        player_search.click()
        # Enter the player name into the search bar
        search_form = self.browser.find_element_by_xpath(
            "//*[@id='header']/div/nav[2]/ul/li[1]/span[1]/input"
        )
        search_form.send_keys(self.player_name)
        # Click the search form to make all the results appear
        search_form.click()
        WebDriverWait(self.browser, self.page_load_timeout, **kwargs).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//*[@id='header']/div/nav[2]/ul/li[1]/span[1]/div")
            )
        )

    def _get_search_results(self) -> Sequence[Tuple[str, str]]:
        """
        Get results from the search
        """
        players = self.browser.find_element_by_xpath(
            "//*[@id='header']/div/nav[2]/ul/li[1]/span[1]/div"
        )
        player_club_list = players.text.split("\n")
        players = zip(player_club_list[::2], player_club_list[1::2])

        return players
