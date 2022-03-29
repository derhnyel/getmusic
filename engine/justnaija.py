from engine.root import BaseEngine


class JustNaija(BaseEngine):
    engine_name = "justnaija"
    summary = None #get summary
    music_category = "music"
    tracks_page_path = "music-mp3"
    allowed_categories = ('album','gospel','throwback','download-mp3','ghana','mixtape','south-africa','west-africa','foreign','tanzania','instrumentals','track')

    def __init__(self):
        super().__init__()
        self.site_uri = "https://justnaija.com/"
        self.request_method = self.GET
    
    def fetch(self, category='track',page=1,**kwargs):
        """Fetch Latest Items Based on Category and Page Number"""
        # Allows a url too
        soup = self.get_response_object(url = self.get_formated_url(url=kwargs.pop('url'),path='',params='') 
            if kwargs.get('url') 
            else self.get_formated_url(
                category=category, 
                page=page, 
                params={},
                **kwargs
                ))
        self.results = self.parse_parent_object(soup,**kwargs)
        return self.results    
    
    # allowed category is album and music only for search  
    def search(self, query='', page=1, category="music", **kwargs):
        """Search Engine with query, page ,category parameters"""

        # Either search through url or search through query
        search_url = self.get_formated_url(url=kwargs.pop('url'),path='',params='' ) if kwargs.get(
            'url') else self.get_formated_url(
            query=query,
            path=["search"], 
            page=page, 
            category=category,
            **kwargs,
        )
        soup = self.get_response_object(url=search_url,**kwargs)
        self.results = self.parse_parent_object(soup, **kwargs)
        return self.results    
    
    def parse_parent_object(self,soup=None,**kwargs):
        """
        Parses Engine Soup for links to individual items 
        and parse those links then pass thier soups to parse single object
        """
        
        return list(
            self.parse_single_object(
                soup=self.get_response_object(
                    elem["href"]), category=
                "album" if ("album-download" in elem["href"] or "mixtape" in elem["href"]) else "track" #check Url to get category of item
                    )
                    for elem in soup.select("main article h3 a") # select a tag to get href
                    )

    def parse_single_object(self, soup=None, category=None,**kwargs):

        """
        Parses the source code to return

        :param : soup: link found in <main article h3 a>
        :type soup: `bs4.element.ResultSet`
        :param : category: album or track or mixtape
        :type category: `str` 
        :return: parsed title, download_link ,category of soup
        :rtype: dict
        """

        #Get Header element from soup which will be used to get the artist and title based on the category
        header_elem = soup.select('div[class="mpostheader"] span[class="h1"]')
        header_elem = header_elem[0] if len(header_elem) >= 1 else soup.select(
            'div[class="mpostheader"] > h1')[0]
        # Some Soups do not have Download links
        try:
            download_link = soup.select('p[class="song-download"] a')[0]["href"]
        except Exception:
            download_link = None
        # Some soups do not have Art / Thumbnails    
        try:
           art_link = soup.select('figure[class="song-thumbnail"] img')[0]["src"]
        except:
            art_link = None  
        # For album category      
        if category == 'album':
            # get artist/title if the exist
            # if any doesnt exist that means the category is mixtape
            tracks_details=[] 
            try:
                artist,title = header_elem.text.split(" | ")[0].split(" – ")
            #set category to mixtape    
            except:
                artist,title = header_elem.text.split(" - ")
                category = 'mixtape'
            #continue with category as album    
            else:
                #select album tracklist and obtain songs title and download_url    
                tracklist_elem = soup.select(
                    'div[class="mu-o-c"] div[class="mu-o-unit-c"] div[class="album-side-1"]'
                )
                
                for track_elem in tracklist_elem:
                    song_link = track_elem.h4.a["href"]
                    song_title = (
                        track_elem.h4.a.text + track_elem.span.text
                        if track_elem.span != None
                        else track_elem.h4.a.text
                    )
                    tracks_details.append((song_title,song_link))
                return dict(type='album',category=category,artist=artist, title=title, category_download=download_link, category_art=art_link, category_tracks_details=tracks_details)
            # eXECUTE FOR MIXTAPES. select MIXTAPES tracklist and obtain songs title and download_url    
            tracklist_elem = soup.select(
                'article[class="song-info"] div[class="details"] br'
            )
            for track_elem in tracklist_elem:
                try:
                    track = ''.join(track_elem.previous_sibling).strip('\r\n')
                    if track in {'Tracklist','','Track List;'}:continue
                except:
                    continue
                tracks_details.append(track)
            return dict(type='album',category=category,artist=artist, title=title, category_art=art_link, category_download=download_link, category_tracks_details=tracks_details)
        try:
            head = header_elem.text.split("] ")[1].split(" – ")
        except:
             head = header_elem.text.split(" – ")   
        #fOR SINGLE TRACKS
        artist,title = head if len(head) is 2 else header_elem.text.split("] ")[1].split(" - ")
        return dict(type='track',category=category,artist=artist, title=title, category_art=art_link, category_download=download_link)

        
    def get_url_path(self,category=None,page=None,**kwargs):
        return (
            (self.tracks_page_path, self.page_path, str(page))
            if category == 'track'
            else
            (self.music_category, category,self.page_path, str(page)
            ))
   
    def get_query_params(self, query=None,page=None,category=None,**kwargs):
        """PAth to Page Content"""
        return {
            'q': query,
            'folder': category,
            'p':page
        }
