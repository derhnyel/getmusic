
from engine.root import BaseEngine
import json
class Mp3Juices(BaseEngine):

    api_path = 'api'
    search_path = 'search.php?'

    def __init__(self):
        super().__init__()
        self.site_uri = "https://myfreemp3juices.cc/"
        self.request_method = self.POST

    def get_query_params(self,query=None,page=None,**kwargs):
        return  dict(q=query,page=page)

    def get_url_path(self, page=None, category=None):
        return (self.api_path,self.search_path)

    def search(self, query=None, page=0, **kwargs):
        response = self.get_response_object(url=self.get_formated_url(**kwargs),payload=self.get_query_params(query=query,page=page))
        response = json.loads(response.text.strip("();\n"))["response"]
        return list(dict(category='track',artist=item["artist"],title=item['title'],category_download=item["url"], track_length=item['duration']/60) for item in response if isinstance(item,dict))
    







      

