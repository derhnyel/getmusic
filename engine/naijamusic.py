
from engine.root import BaseEngine


class NaijaMusic(BaseEngine):
    #create_Enum
    engine_name = "naijamusic"
    page_path = "page"
    categories = ('albums-eps', 'new','mixtape','gospel','south-african-music','ghana')

    def __init__(self):
        super().__init__()
        self.site_uri = "https://www.naijamusic.com.ng/"
        self.request_method = self.GET


    def get_url_path(self, page=None, category=None):
        return (category, self.page_path, str(page)) 


    def parse_parent_object(self,soup,**kwargs):
        return list(elem['href'] for elem in soup.select("article h2 a"))
    
    #change to fetch 
    def search(self, query=None, page=1, category='new', **kwargs):
        soup = self.get_response_object(url=kwargs.pop('url') if kwargs.get(
            'url') else self.get_formated_url(category=category, page=page, params={}, **kwargs))  
        return self.parse_parent_object(soup,**kwargs)

    def parse_single_object(self, soup, category=None, **kwargs):
        #some albums li have href while others dont
        #logic to extract download_link,artist,title for all
        #only difference is that for tracks the soupis passed directly here
        # for albums each url is parsed and passed to this function
        return 

