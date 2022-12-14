import requests
from loguru import logger
from requests.utils import requote_uri
from typing import List, Dict, Union
from concurrent.futures import ThreadPoolExecutor


class UrlAvailabilityChecker:

    def __init__(self, urls: List[str], max_workers=50, timeout=3):
        self.urls = urls
        self.max_workers = max_workers
        self.timeout = timeout

        self.result_status_codes: Dict[str, int] = {}
        self.result_unshorten_urls: Dict[str, str] = {}

    def get_status_code(self, url: str) -> Union[int, None]:
        try:
            response = requests.head(url, timeout=self.timeout)
            logger.info(f"Pinging the {url}...")
            return response.status_code
        except requests.Timeout:
            return 404

    def get_unshorten_url(self, url: str) -> Union[str, None]:
        try:
            response = requests.get(url, timeout=self.timeout)
            logger.info(f"Getting an unshorten url: {response.url}")
            return response.url
        except requests.Timeout:
            logger.error(f"Request failed due timeout url: {url}")
            return None

    @staticmethod
    def _replace_layer_protocol(url: str) -> str:
        return url.replace("http://", "").replace("https://", "").replace("www.", "")

    def _check_website(self, url: str) -> None:
        self.result_status_codes[url] = self.get_status_code(url)
        unshorten_url = self.get_unshorten_url(url)
        if unshorten_url and \
                self._replace_layer_protocol(unshorten_url) != self._replace_layer_protocol(url):
            self.result_unshorten_urls[url] = self.get_unshorten_url(url)

    def start_threads(self) -> None:
        logger.info(f"Start ThreadPoolExecutor")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for url in self.urls:
                uri = requote_uri(url)
                executor.submit(self._check_website, uri)
        logger.info(f"End ThreadPoolExecutor")
