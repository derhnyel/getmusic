
import helpers
from urllib.parse import urlparse,urlencode
import asyncio
from bs4 import BeautifulSoup as bs4
from abc import ABCMeta,abstractmethod
import json

# class Response:

#     def __init__(self, data):
#         self.__dict__ = json.loads(data)

# response = Response(json_data)

# if hasattr(response , 'url'):
class RootSearch():
    __metaclass__ = ABCMeta
    items = {}
    engine_name= None
    formated_url = None
    site_uri = None
    request_method = None
    GET,POST = 'get','post'
    response_type = None
    JSON,HTML = 'json','html'
    ALBUM,MUSIC,TRACK  = 'albums','music','tracks'

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
          
    async def get_object(self,url=None,method=None,payload=None,html_page=None,json_object=None):
        if url != None:
            source = await self.get_page_content(url,method=method,payload=payload)
            """Set default else to html"""
            if  self.response_type == self.HTML:
                return bs4(source,'html')
            """else a json object shoud be returned unpacked""" 
        elif html_page != None:
               return bs4(html_page,'html')
        elif json_object != None:
            """unpack json """

        else:
            raise Exception ('ERROR: {}\n'.format("<get_object> requires either a url / html_page content / json object"))       


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
    
    def result(self,object,infant=False,category=None,**kwargs): 
        """Implement for get both json and soup objects"""
        # if child:
        #     child_result = self.parse_child_obejct(soup,category=category,**kwargs)   
        for child in self.parse_parent_object(object):
            if helpers.isvalid_url(child):
                #self.request
                result = self.parse_object(child,url=True)
            elif helpers.isvalid_json(child):
                #self.get_object(html_page=child)
                """Unpack Json data"""
            elif isinstance(str,child):
                #self.get_object(json_object=child)
                """Parse str object as bs4 soup"""    
    
    def get_query_params(self,query=None,**kwargs):
        """Should be overwritten if engine needs query params"""
        return {'q':query}

    def get_url_path(self,page=None,category=None):
        """Should be overwritten if engine needs url paths"""
        return 
           
    def parse_parent_object(self,parent_object):

        """Override if engine needs to parse parent object"""
        return [parent_object]
        #return " Children objects(links/soup/json)"
    
    @abstractmethod
    def parse_object(self,object,category=None,url=False,json=False,soup=False,**kwargs):
        raise NotImplementedError(
            "subclasses must define method <parse_object>")
        #return "All details in child soup (child_result)"
            


        








        