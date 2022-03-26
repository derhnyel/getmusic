from engine.root import BaseEngine
import json

class FreeMp3(BaseEngine):
    
    def __init__(self):
        super().__init__()
        self.site_uri = "https://backendace.1010diy.com/"
        self.request_method = self.GET
    

    def get_url_path(self,page=None,category=None,**kwargs):
        return('web','free-mp3-finder','query')

    def get_query_params(self, query=None, page=None, **kwargs):
        return dict(q=query,type='youtube',pageToken='')

    def search(self, query=None, page=None, **kwargs):
        response = self.get_response_object(
            url=self.get_formated_url(
                query=query,
                **kwargs),
                **kwargs,
        )
        response = json.loads(response.text.strip("</iframe"))
        #Get artist and song Title duration too try/except split with #"-"
        youtube_links = list(self.parse_parent_object(item['url']) for  item in response['data']['items'])
        return youtube_links


    def parse_parent_object(self,link,**kwargs):
        #get file size, audio quality ,extension
        details_url = self.get_formated_url(
            url="https://backendace.1010diy.com/",
            params = {'url':link},
            method = self.GET,\
            path=("web","free-mp3-finder","detail"),
        )
        response = self.get_response_object(
            url=details_url,
            **kwargs,
        )
        response = json.loads(response.text)['data']['audios']
        
        [self.parse_child_object(item['url']) item for item in response]

   def parse_child_object(self,link,**kwargs):
       #get download link
       download_link  = self.get_formated_url(
            url="https://stream_ace1.1010diy.com/",
            params = {},
            method = self.GET,
            path=([link]),
        )
        return download_link






