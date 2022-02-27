
import helpers
from urllib.parse import urlparse
import asyncio
from bs4 import BeautifulSoup as bs4
from abc import ABCMeta,abstractmethod

class RootFetch():
    __metaclass__ = ABCMeta
    items = {}
    formated_url = None
    site_uri = None
    
    
    def get_formated_url(self,page=None,category=None):
        url = urlparse(self.site_uri)
        url_path = helpers.join_url_path(self.get_url_paths(page,category))
        self.formated_url = url._replace(path=url_path)
        return self.formated_url.geturl()
    

   
    def get_header(self):
        headers = {
            "Cache-Control": 'no-cache',
            "Connection": "keep-alive",
            "User-Agent": helpers.gen_user_agent()
        }
        return headers    
    
    async def get_page_content(self,url):
        #request url
        return "html source page"
          
    async def get_soup_object(self,url):
        source = await self.get_page_content(url)
        return bs4(source,'html')

    def request(self,url):
        loop = asyncio.get_event_loop()       
        return loop.run_until_complete(self.get_soup_object(url))
    
    def fetch(self,page = 1,category= None,**kwargs):
        url = self.get_formated_url(page=page,category=category) 
        result = self.result(soup=self.request(url),category=category)
        if kwargs.get("url"):
            url = kwargs.pop("url")
            result = self.result(soup=self.request(url),child=True,category=category)
    
    @abstractmethod
    def parse_child_result(self,child_soup,category=None):
        raise NotImplementedError(
            "subclasses must define method <parse_child_result>")
        #return "All details in child soup (child_result)"
   
    @abstractmethod
    def parse_parent_soup(self,parent_soup):
        raise NotImplementedError(
            "subclasses must define method <parse_parent_soup>")
        #return " Children urls(links)"
    
    @abstractmethod
    def get_url_paths(self, page=None,category=None):
        raise NotImplementedError(
            "subclasses must define method <get_url_paths>")
        #return  """ get url paths """    
        

    def result(self,soup,child=False,category=None):
        if child:
            child_result = self.parse_child_result(soup,category=category)   
        for infant in self.parse_parent_soup(soup):
            child_result = self.parse_child_result(self.request(infant),category=category)
            


        








        