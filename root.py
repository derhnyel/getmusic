
import helpers
from urllib.parse import urlparse,urlencode
import asyncio
from bs4 import BeautifulSoup as bs4
from abc import ABCMeta,abstractmethod

class RootFetch():
    __metaclass__ = ABCMeta
    items = {}
    engine_name= None
    formated_url = None
    site_uri = None
    request_method = None
    GET = 'get'
    POST = 'post'
    response_type = None
    JSON = 'json'
    HTML = 'html'
    
    def get_formated_url(self,page=None,category=None,query=None,method=None,**kwargs):
        url = urlparse(self.site_uri)
        url_path = helpers.join_url_path(self.get_url_path(page,category))
        self.formated_url = url._replace(path=url_path,query=urlencode(self.get_query_params(query,**kwargs))) if method==self.GET else url._replace(path=url_path)
        return self.formated_url.geturl()
       
    def get_header(self):
        headers = {
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "User-Agent": helpers.gen_user_agent()
        }
        return headers

    async def get_page_content(self,url,method=None,payload=None):
        if  method == self.GET:
            #aiohttp request url(GET)
            return "html/json objcet"
        #aiohttp request url (POST) with payload
        return "html/json object"    
          
    async def get_object(self,url,method=None,payload=None):
        source = await self.get_page_content(url,method=method)
        """Set default else to html"""
        if  self.response_type == self.HTML:
            return bs4(source,'html')
        """else a json object shoud be returned"""        

    def request(self,url,method=None,payload=None):
        loop = asyncio.get_event_loop()       
        return loop.run_until_complete(self.get_object(url,method=method,payload=payload))  
    
    def search(self,query=None,page=None,category=None,**kwargs):
        method = self.request_method
        url = self.get_formated_url(page=page,category=category,query=query,method=method)
        """Set default else to get"""
        if method == self.GET:
            result = self.result(self.request(url,method=method),category=category)
            """Try something else"""
            # if kwargs.get("url"):
            #     url = kwargs.pop("url")
            #     result = self.result(soup=self.request(url,method=method),child=True,category=category)
        result = self.result(self.request(url,method=method,payload=self.get_query_params(query,**kwargs)),category=category)       
    
    def result(self,object,child=False,category=None,**kwargs):
        """Implement for get both json and soup objects"""
        # if child:
        #     child_result = self.parse_child_obejct(soup,category=category,**kwargs)   
        # for infant in self.parse_parent(soup):
        #     child_result = self.parse_child_object(self.request(infant),category=category,**kwargs) 
    
    def get_query_params(self,query=None,**kwargs):
        """Should be overwritten if engine needs query params"""
        return {'q':query}

    def get_url_path(self,page=None,category=None):
        """Should be overwritten if engine needs url paths"""
        return 
           
    @abstractmethod
    def parse_parent_object(self,parent_object):
        """Implement to Parse both json and html"""
        raise NotImplementedError(
            "subclasses must define method <parse_parent>")
        #return " Children objects(links/raw_html/json)"
    
    @abstractmethod
    def parse_child_object(self,child_object,category=None,**kwargs):
        raise NotImplementedError(
            "subclasses must define method <parse_child_object>")
        #return "All details in child soup (child_result)"
            


        








        