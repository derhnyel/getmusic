import requests
import pdb
import asyncio
import aiohttp

from urllib.parse import urlparse, urlencode
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup as bs4


import utils.helpers as helpers


class BaseEngine(ABC):
    """
    Search base to be extended by search engine
    Every subclass must have two methods `search` amd `parse_single_object`
    
    """

    #TODO: Create an Enum For some objects and results Items
    #TODO: Create a Caching System for results -> SpeedUp Engine
    #TODO: Handle Engine Errors and Exceptions
    #TODO: Make Request Handling Asynchronous -> SpeedUp Engine
    #TODO: Seperate Engine's parse single object method from search method -> SpeedUp Engine
    #TODO: ADD more Music Engines
    #TODO: Scrap some Engines For more Track details 
    #TODO: Put Summary For every Engine


    summary = None
    
    #Name of the Music Engine
    engine_name=None
    
    #Basically just allowed url paths which can be queried
    allowed_categories=None

    # Music Engine unformatted URL
    site_uri = None
    
    # Music Engine request method. Can be either Post or GEt
    request_method = None 
    GET, POST = "get", "post"

    # The url path to each page
    page_path = "page"

    # The formatted with a query params Set 
    formated_url = None
    
    # Music Search or Fetch Engine Results
    results=None

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def search(self, query=None, page=None, category=None,**kwargs):
        """
         Query the Music search engine

        :param query: the query to search for
        :type query: str
        :param page: Page to be displayed, defaults to 1
        :type page: int
        :param category: search filter 
        :type category: str
        :return: dictionary. Containing titles,category,category_download.
        """
        #Each engines implements it's own searching style
        raise NotImplementedError()

    @abstractmethod
    def parse_single_object(self, object=None,**kwargs):
        """Parse Every Response Object to retrieve category_download,category,titles """
        #Each engine should have its own fetch single objects defined"""
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

        # print("\nFORMATED URL: "+self.formated_url.geturl())
        return self.formated_url.geturl()


    def get_response_object(self,url,method=None,payload=None,header=None,**kwargs):
        """
        Returns the source code of a webpage.

        :rtype: Json/soup
        :param url: URL to pull it's source code
        :method: str -> request method post/get
        :payload: dict -> A payload For post requests
        :header: dict -> The request header
        :return: Html source code or Json of a given URL.
        """
        # print("\n\n\nRESPONSE FROM URL :  "+url)

        # Get header and method either passed into the get_response_object or globally set
        header= helpers.get_header() if header is None else header
        method = self.request_method if method is None else method
        # Handle request based on Request method post and get
        if method==self.POST:
            return requests.request("POST",url,headers=header,data=payload)
        webpage = requests.get(url, headers=header)
        soup = bs4(webpage.content, "html.parser")
        return soup

    async def fetch_webpage(
            self, session: aiohttp.ClientSession, url: str, method=None): 
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
                return await response.text('utf-8')
            else:
                return None

    def parse_webpage(self, webpage):
        """
        Returns a beautiful soup object of the webpage
 
        :rtype: BS4 object
        :webpage html from a url
        """
        soup = bs4(webpage, "html.parser")
        return soup

    def get_query_params(self, query=None,page=None,category=None,**kwargs):
        """ This  function should be overwritten to return a dictionary of query params"""
        return {"q": query}

    def get_url_path(self, page=None, category=None,**kwargs):
        """Should be overwritten if engine needs url paths"""
        return

    def parse_parent_object(self, parent_object=None,**kwwargs):
        """Every div/span/json containing link to the single object which
           could then be fetched passed into parse single object to retrieve objects tiltle,download link,etc """
        # Override if engine needs to parse parent object"""
        return
