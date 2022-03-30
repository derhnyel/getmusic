
from engine.root import BaseEngine


class NaijaMusic(BaseEngine):
    engine_name = "naijamusic"
    summary = None #get summary information
    allowed_categories = ('albums-eps', 'new','mixtape','gospel','south-african-music','ghana','tag')

    def __init__(self):
        super().__init__()
        self.site_uri = "https://www.naijamusic.com.ng/"
        self.request_method = self.GET

    def fetch(self, category='new',page=1, **kwargs):

        """Fetch Latest Items Based on Category and Page Number"""
        #Allows a url too
        soup = self.get_response_object(url = self.get_formated_url(url=kwargs.pop('url'),path='',params='') if kwargs.get(
            'url') else self.get_formated_url(category=category, page=page, params={}, **kwargs))  
        self.results = self.parse_parent_object(soup,category=category,**kwargs)
        return self.results
                

    def search(self, query='', page=1, category='tracks', **kwargs):

        """Search Engine with query, page ,category parameters"""

        # Either search through url or query 
        # categories are like filters
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

    def parse_parent_object(self,soup=None,category=None,**kwargs):
        """
        Parses Engine Soup for links to individual items 
        and parse those links then pass thier soups to parse single object
        """
        return list(self.parse_single_object(
                soup = self.get_response_object(url=elem['href'],**kwargs),
                category=category,
                referer=elem['href'],
                **kwargs,) 
            for elem in soup.select("article h2 a"))
            
            #TODO: Filter Gist,and Videos in search results if not (elem.select(
                # 'div[class="post-meta-items meta-below"] a')[0].text == "Gist" or 
                # elem['href'].split('/')[3].startswith('video') and 
                # elem.text.split(':')[0] =='VIDEO')
                # To download mp3 the request header has to contain {'referer': url}

    def parse_single_object(self, soup, category=None,referer=None,**kwargs):
        """
        Parses the source code to return

        :param : soup: link found in <article h2 a>
        :type soup: `bs4.element.ResultSet`
        :param : category: album or track 
        :type category: `str`
        :param : referer: url to page. needed for request header to download file 
        :type referer: `str`
        :return: parsed title, download_link ,category of soup
        :rtype: dict
        """
        # ALL Songs on NaijaMusic have thier individual url even all the tracks in an album

        # Some div contain title and Artist while some do not
        try:
            artist,title = soup.select(
                    'div[class="the-post-header s-head-modern s-head-large"] h1[class="is-title post-title"]')[0].text.split(" – ")
        except:
             artist = title = soup.select(
                    'div[class="the-post-header s-head-modern s-head-large"] h1[class="is-title post-title"]')[0].text  

        # GEt the art link         
        art_link = 'https:{link}'.format(link=soup.select(
                'div[class="post-content cf entry-content content-spacious"] picture img')[0]['data-lazy-src'])

        # Album / Eps on NaijaMusic usually have tracks leading to their individual Pages
        # Pages are parsed seperately to extract download link via the get_download_link method        
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
                    #Some elements do not have download link
                    download_link = None
                finally:    
                    tracklist.append((song_title,download_link))
            return dict(type = 'album', category = category,artist = artist, title = title,download=None,art = art_link,details = tracklist)
        #for single tracks
        download_link = self.get_download_link(soup,referer,**kwargs)
        return dict(
            type = 'track',
            category = category, 
            artist = artist, 
            title = title, 
            download = download_link,
            art = art_link
            )
      
    def get_download_link(self,soup,referer=None,**kwargs):
        """Get Indivial download link from URL"""
        download_elem = soup.select('audio[class="wp-audio-shortcode"]')
        return None if len(download_elem)<1 else (download_elem[0].a['href'],referer)
                           
    def get_url_path(self, page=None, category=None):
        """PAth to Page Content"""
        return (category, self.page_path, str(page))  

    def get_query_params(self, query=None, **kwargs):
        return {
            's': query
        }