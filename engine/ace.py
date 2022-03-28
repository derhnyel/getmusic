from engine.root import BaseEngine
import json

class Ace(BaseEngine):
    
    def __init__(self):
        super().__init__()
        self.site_uri = "https://backendace.1010diy.com/"
        self.request_method = self.GET
    

    def get_url_path(self,**kwargs):
        return('web','free-mp3-finder','query')

    def get_query_params(self, query=None, **kwargs):
        return dict(q=query,type='youtube',pageToken='')
    
    #AN API SO URL NOT ALLOWED
    def search(self, query='', **kwargs):
        response = self.get_response_object(
            url=self.get_formated_url(
                query=query,
                **kwargs),
                **kwargs,
        )
        response = json.loads(response.text.strip("</iframe"))
        #Get artist and song Title duration too try/except split with #"-"

        self.results = list(dict(
            title=item['title'],
            #artist = item['title'][0] if len(item['title'].split(" - ")) > 1 else item['title'],
            category ='track',
            track_lenght=item['duration'],
            category_art=item['thumbnail'],
            category_video_palyer= item['player'],
            category_details=self.parse_parent_object(item['url'],title=item['title'])) for  item in response['data']['items'])
        return self.results    


    def parse_parent_object(self,link=None,title=None,**kwargs):
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
        response = json.loads(response.text)['data']['audios'] + json.loads(response.text)['data']['videos']
        
        return list(dict(
            file_size=item['fileSize'],
            quality=item['formatNote'],
            type='track' if item['ext'] in ['mp3', 'ogg','wav',] else 'video' if item['ext'] in ['mp4'] else None,
            category_download=self.parse_single_object(
                item['url'],
                title,
                item['ext'],
                **kwargs)) 
            for item in response)

    def parse_single_object(self,link=None,title=None,category_type=None,**kwargs):         
        return link if link.startswith('https://') else "https://stream_ace1.1010diy.com/{url}&ext={ext}&title={title}".format(url=link,ext=category_type,title=title),





