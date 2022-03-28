
from engine.root import BaseEngine


class NaijaMusic(BaseEngine):
    #create_Enum
    engine_name = "naijamusic"
    page_path = "page"
    allowed_categories = ('albums-eps', 'new','mixtape','gospel','south-african-music','ghana','tag')

    def __init__(self):
        super().__init__()
        self.site_uri = "https://www.naijamusic.com.ng/"
        self.request_method = self.GET

    def get_url_path(self, page=None, category=None):
        return (category, self.page_path, str(page)) 


    def parse_parent_object(self,soup=None,category=None,**kwargs):
        return list(self.parse_single_object(
                soup = self.get_response_object(url=elem['href'],**kwargs),
                category=category,
                referer=elem['href'],
                **kwargs,) 
            for elem in soup.select("article h2 a"))
            
            #TODO Filter Gist,and Videos in search results if not (
                #elem.select(
                    #'div[class="post-meta-items meta-below"] a')[0].text == "Gist" or 
                    ##elem['href'].split('/')[3].startswith('video') and 
                    #elem.text.split(':')[0] =='VIDEO')
                

    def search(self, query=None, page=1, category='tracks', **kwargs):
        search_url = self.get_formated_url(url=kwargs.pop('url'),path='',params='' ) if kwargs.get(
            'url') else self.get_formated_url(
            query=query,
            path=(
                self.page_path, str(page)),
                page=page,
                category=category,
                **kwargs,
            ) if category != 'artist' else self.get_formated_url(
                query='',
                path=(
                    'tag',
                    query,
                    self.page_path, str(page)),
                page=page,
                category=category,
                params ={},
                **kwargs,
            ) 
        soup = self.get_response_object(url=search_url,**kwargs)
        self.results = self.parse_parent_object(soup,category=category,**kwargs)
        return self.results

    def get_query_params(self, query=None, **kwargs):
        return {
            's': query
        }

    #change to fetch 
    #header={'referer': url} when downloading file
    def fetch(self, category='new',page=1, **kwargs):
        soup = self.get_response_object(url = self.get_formated_url(url=kwargs.pop('url'),path='',params='') if kwargs.get(
            'url') else self.get_formated_url(category=category, page=page, params={}, **kwargs))  
        self.results = self.parse_parent_object(soup,category=category,**kwargs)
        return self.results
    
    def get_download_link(self,soup,referer=None,**kwargs):
        download_elem = soup.select('audio[class="wp-audio-shortcode"]')
        return None if len(download_elem)<1 else (download_elem[0].a['href'],referer)


    def parse_single_object(self, soup, category=None,referer=None,**kwargs):
        try:
            artist,title = soup.select(
                    'div[class="the-post-header s-head-modern s-head-large"] h1[class="is-title post-title"]')[0].text.split(" – ")
        except:
             artist=title = soup.select(
                    'div[class="the-post-header s-head-modern s-head-large"] h1[class="is-title post-title"]')[0].text           
        art_link = 'https:'+soup.select(
                'div[class="post-content cf entry-content content-spacious"] picture img')[0]['data-lazy-src']
        if category=='albums-eps':
            tracklist_elem = soup.select('div[class = "post-content cf entry-content content-spacious"] ul li')
            tracklist =[]
            for elem in tracklist_elem:
                try:
                    song_title=elem.text
                    download_link = elem.a['href'] if elem.a['href'].endswith('.mp3') else self.get_download_link(
                        self.get_response_object(url=elem.a['href'],**kwargs),
                        referer = elem.a['href'],
                        **kwargs)
                except Exception as e:
                    download_link = None
                finally:    
                    tracklist.append((song_title,download_link))
            return dict(type = 'album', category = category, artist = artist, title = title, category_download =None, category_art = art_link, category_tracks_details = tracklist)
        download_link = self.get_download_link(soup,referer,**kwargs)
        return dict(type = 'track', category = category, artist = artist, title = title, category_download = download_link, category_art = art_link)
                           

