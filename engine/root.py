import requests
import asyncio

import json

from urllib.parse import urlparse, urlencode
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as bs4

import utils.helpers as helpers


class BaseEngine(ABC):
    #create an enum object for this
    site_uri = ""
    GET, POST = "get", "post"
    ALBUM, MUSIC, TRACK = "albums", "music", "tracks"
    request_method = None

    def get_formated_url(
        self, url=None,path=None,page=None, category=None, query=None, method=None,params=None, **kwargs):
        url = urlparse(self.site_uri) if url is None else urlparse(url)
        url_path = helpers.join_url_path(self.get_url_path(page, category)) if path is None else helpers.join_url_path(path)
        params = self.get_query_params(query, **kwargs) if params is None else params
        method = self.request_method if method is None else method
        self.formated_url = (
            url._replace(
                path=url_path, query=urlencode(params)
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

    @abstractmethod
    def search(self, query=None, page=None, category=None, **kwargs):
        """Each engines implements it's own searching style"""
        raise NotImplementedError()

    def get_response_object(self,url,method=None,payload=None,**kwargs):
        header= self.get_header()
        method = self.request_method if method is None else method
        if method==self.POST:
            #function to identify response type and parse accordingly
            return requests.request("POST",url,headers=header,data=payload).json() 
        webpage = requests.get(url, headers=header)
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
        return parent_object
