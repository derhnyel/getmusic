
from engine.root import BaseEngine
class Mp3Juices(BaseEngine):

    api_path = 'api/search.php'

    def __init__(self):
        super().__init__()
        self.site_uri = "https://myfreemp3juices.cc/"
        self.request_method = self.POST

    def get_query_params(self,query=None,page=None,**kwargs):
        if kwargs.get("id"):
            return dict(id=kwargs.pop(id))
        return  dict(q=query,page=page)

    def get_url_path(self, page=None, category=None):
        return (self.api_path)

    def parse_parent_object(self,json,**kwargs):
        #extract songs id from json
        #extract song art
        # track details
        return

    def parse_single_object(self,id=None,category=None,**kwargs):
        return self.get_formated_url(
            self,
            url = "https://idmp3s.com/",
            params = self.get_query_params(**{'id':id}),
            method = self.GET,path=("api/vip/get_song.php"),
        )

    def search(self, query=None, page=None, category=None, **kwargs):
        json = self.get_soup(url=self.get_formated_url(**kwargs),payload=self.get_query_params(query=query,page=0))
        response = self.parse_parent_object(json)        
        return response
         







      

