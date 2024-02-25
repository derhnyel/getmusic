import (
    request,
    pdb,
    asyncio,
    aiohttp
)

from urllib.parse import urlparse, urlencode
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as bs4
from typing import List, Tuple
import utils.helpers as helpers


class BaseEngine(ABC):
    """
    Base engine from which others engine subclasses
    """

    # Engine properties
    summary: str = None
    name: str = None
    categories: Tuple[str] = []
    site_uri: str = None
    request_methods = None
    formated_url = None
    GET, POST = "get", "post"

    @abstractmethod 
    def search(
        self, query: str=None, page: str=None, 
        category: str=None,**kwargs
        ):
        """ 
        Method to query a particular engine
        """
        raise NotImplementedError()

    def get_formated_url(
        self,url=None,path=None,
        page=None, category=None, 
        query=None, method=None,
        params=None, **kwargs
        ):
        """
        Return a formatted Music Engine search or fetch url
        """
        # Url could be set to default site Url or A custom url can be inputted 
        url = urlparse(self.site_uri) if url is None else urlparse(url)
        
        # Get Url paths and Query Params based on custom path or params passed in or the get_url_path/get_query_params method 
        url_path = helpers.join_url_path(self.get_url_path(
            page=page,category=category,**kwargs)
            ) if path is None else helpers.join_url_path(path)    
        
        params = self.get_query_params(
            query=query,
            page=page,
            category=category,
            **kwargs) if params is None else params
        
        # Defined request method to Get/Post and use queries where applicable     
        method = self.request_method if method is None else method
        self.formated_url = (
            url._replace(
                path=url_path, query=urlencode(params)
            )
            if method == self.GET
            else url._replace(path=url_path)
        )

        return self.formated_url.geturl()


    @helpers.force_async
    def get_response_objet(
            self, session: aiohttp.ClientSession, url: str, method=None, payload=None): 
        """
        Returns the source source code of a webpage, if it exist or None.

        :rtype
        :session: resusable aiohttp.ClientSession
        :param url: URL to pull it's source code
        :method: str -> request method post/get
        :payload: dict -> A payload For post requests
        :header: dict -> The request header
        :return: Html source code or Json of a given URL.
        """
        
        if method == self.POST:
            pass  
        # Get url asynchronously 
        async with session.get(url) as response:
            if response.status == 200: 
                webpage = response.text('utf-8')    
                soup = bs4(webpage, "html.parser")
                return soup
            else:
                return None


        
