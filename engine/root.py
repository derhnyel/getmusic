import requests
import asyncio

import json

from urllib.parse import urlparse, urlencode
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as bs4
from fake_useragent import UserAgent

import utils.helpers as helpers


class BaseEngine(ABC):
    site_uri = ""
    GET, POST = "get", "post"
    ALBUM, MUSIC, TRACK = "albums", "music", "tracks"

    def get_formated_url(
        self, page=None, category=None, query=None, method=None, **kwargs
    ):
        url = urlparse(self.site_uri)
        url_path = helpers.join_url_path(self.get_url_path(page, category))
        self.formated_url = (
            url._replace(
                path=url_path, query=urlencode(self.get_query_params(query, **kwargs))
            )
            if method == self.GET
            else url._replace(path=url_path)
        )
        return self.formated_url.geturl()

    def get_header(self):
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "User-Agent": helpers.gen_user_agent(),
        }
        return headers

    def request(self, url, method=None, payload=None):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(
            self.get_object(url, method=method, payload=payload)
        )

    @abstractmethod
    def search(self, query=None, page=None, category=None, **kwargs):
        """Each engines implements it's own searching style"""
        raise NotImplementedError()

    def get_soup(self, url):
        UAgent = UserAgent()
        webpage = requests.get(url, headers={"User-Agent": UAgent.random})
        soup = bs4(webpage.content, "html.parser")
        return soup

    def result(self, object, infant=False, category=None, **kwargs):
        """Implement for get both json and soup objects"""

    def get_query_params(self, query=None, **kwargs):
        """Should be overwritten if engine needs query params"""
        return {"q": query}

    def get_url_path(self, page=None, category=None):
        """Should be overwritten if engine needs url paths"""
        return

    def parse_parent_object(self, parent_object):

        """Override if engine needs to parse parent object"""
        return [parent_object]
