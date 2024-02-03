
from engine.root import BaseEngine
import json

class Mp3Juices(BaseEngine):

    engine_name = "Mp3Juices"
    summary = None #Get Summary

    def __init__(self):
        super().__init__()
        self.site_uri = "https://myfreemp3juices.cc/"
        self.request_method = self.POST


    # An API So URL NOT ALLOWED
    def search(self, query='', page=1, **kwargs):
        """Search Engine with query parameter"""
        #get response object from formated url with query
        
        import pdb; pdb.set_trace()
        response = self.get_response_object(
            url = self.get_formated_url(**kwargs),
            payload = self.get_query_params(
                query=query,
                page=page-1,
                **kwargs
                )
            )
        # get details from json Response    
        response = json.loads(response.text.strip("();\n"))["response"]
        self.results= self.parse_single_object(response,**kwargs)
        return self.results

    def parse_single_object(self,json_response=None,**kwargs):
        """
        Parses the source code to return

        :param : json_response: link found in <article h2 a>
        :type json_response: `json`
        :return: category ,download_link,title
        :rtype: list of dict

        """

        #Extract track details from json
        return list(dict(
            art = None,
            category = 'tracks',
            type = 'track',
            artist = item["artist"],
            title = item['title'],
            download = item["url"],
            details = (item['title'],item["url"]),
            duration = item['duration']/60,) 
            for item in json_response if isinstance(item,dict)
            )           

    def get_query_params(self,query=None,page=None,**kwargs):
        return  dict(
            q=query,
            page=page
            )

    def get_url_path(self, page=None, category=None,**kwargs):
        """PAth to Page Content"""
        return ('api', 'search.php?')
    
 
    







      

