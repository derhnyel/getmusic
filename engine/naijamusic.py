
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


    def parse_parent_object(self,soup=None,category=None,**kwargs):
        return list(self.parse_single_object(
            self.get_response_object(
                url=elem['href'])
                ,**kwargs),
            category=category)
            for elem in soup.select("article h2 a"))
        # get soup of links
        # if???? some albums li have href while others dont this is to select song_titles and links in album page
    
    #change to fetch 
    def search(self, query=None, page=1, category='new', **kwargs):
        soup = self.get_response_object(url=kwargs.pop('url') if kwargs.get(
            'url') else self.get_formated_url(category=category, page=page, params={}, **kwargs))  
        return self.parse_parent_object(soup,**kwargs)
    
    def get_download_link(self,soup,**kwargs):
        return

    def parse_single_object(self, soup, category=None, **kwargs):
        artist,title = soup.select(
                'div[class="the-post-header s-head-modern s-head-large"] h1[class="is-title post-title"]')[0].text.split(" – ")
        art_link = 'https:' +
                    soup.select(
                'div[class="post-content cf entry-content content-spacious"] picture img')[0]['data-lazy-src']
        if category=='albums-eps':
            tracklist_elem = soup.select('div[class = "post-content cf entry-content content-spacious"] ul li')
            tracklist =[]
            for elem in tracklist_elem:
                try:
                    song_title = elem.text
                    download_link=self.get_download_link(
                        self.get_response_object(
                            url=elem.a['href'], 
                            **kwargs),
                        **kwargs)
                except TypeError:
                    download_link = None
                tracklist.append((song_title,download_link))
            return dict(type = 'album', category = category, artist = artist, title = title, category_download = None, category_art = art_link, category_tracks_details = tracklist)
        download_link = self.get_download_link(soup)
        return dict(type = 'track', category = category, artist = artist, title = title, category_download = download_link, category_art = art_link)


        
        # logic to extract download_link,artist,title for all (div class="the-post-header s-head-modern s-head-large h1 class="is-title post-title") text split with 
        # only difference is that for tracks category the soup is passed directly here
        # for albums category each url is parsed and passed to this function
        # if ??? or select the google ad block (div class="code-block code-block-14") the use .previous_sibling
        return 

