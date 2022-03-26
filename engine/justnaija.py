from engine.root import BaseEngine


class JustNaija(BaseEngine):
    #create Enum
    engine_name = "justnaija"
    page_path = "page"
    music_category = "music"
    tracks_page_path = "music-mp3"
    
    categories = ('gospel','throwback','download-mp3','ghana','mixtape','south-africa','west-africa','foreign','tanzania','instrumentals','track')

    def __init__(self):
        super().__init__()
        self.site_uri = "https://justnaija.com/"
        self.request_method = self.GET

    def get_url_path(self,category=None,page=None,**kwargs):
        return (
            (self.tracks_page_path, self.page_path, str(page))
            if category == 'track'
            else
            (self.music_category, category,self.page_path, str(page)
            ))
          
    def search(self, query=None, page=1, category="music", **kwargs):
        search_url = self.get_formated_url(
            query=query,
            path=["search"], 
            page=page, 
            category=category,
            **kwargs,
        )
        soup = self.get_response_object(url=search_url,**kwargs)
        return self.parse_parent_object(soup, **kwargs)

    def get_query_params(self, query=None,page=None,category=None,**kwargs):
        return {
            'q': query,
            'folder': category,
            'p':page
        }

    def fetch(self, category='track',page=1,**kwargs):
        soup = self.get_response_object(
            url=kwargs.pop('url') 
            if kwargs.get('url') 
            else self.get_formated_url(
                category=category, 
                page=page, 
                params={},
                **kwargs
                ))
        return self.parse_parent_object(soup,**kwargs)        

    def parse_parent_object(self,soup=None,**kwargs):
        return list(
            self.parse_single_object(
                soup=self.get_response_object(
                    elem["href"]), category=
                "album" if ("album-download" in elem["href"] or "mixtape" in elem["href"]) else "track"
                    )
                    for elem in soup.select("main article h3 a")
                    )

    def parse_single_object(self, soup=None, category=None,**kwargs):
        header_elem = soup.select('div[class="mpostheader"] span[class="h1"]')
        
        header_elem = header_elem[0] if len(header_elem) >= 1 else soup.select(
            'div[class="mpostheader"] > h1')[0]
        print(header_elem.text)
        try:
            download_link = soup.select('p[class="song-download"] a')[0]["href"]
        except Exception:
            download_link = None
        try:
           art_link = soup.select('figure[class="song-thumbnail"] img')[0]["src"]
        except:
            art_link = None   
        if category == 'album':
            try:
                artist,title = header_elem.text.split(" | ")[0].split(" – ")
            except:
                artist,title = header_elem.text.split(" - ")
                category = 'mixtape'
            else:    
                tracklist_elem = soup.select(
                    'div[class="mu-o-c"] div[class="mu-o-unit-c"] div[class="album-side-1"]'
                )
                tracks_details=[]
                for track_elem in tracklist_elem:
                    song_link = track_elem.h4.a["href"]
                    song_title = (
                        track_elem.h4.a.text + track_elem.span.text
                        if track_elem.span != None
                        else track_elem.h4.a.text
                    )
                    tracks_details.append((song_title,song_link))
                return dict(type='album',category=category,artist=artist, title=title, category_download=download_link, category_art=art_link, category_tracks_details=tracks_details)
            track_list = []
            tracklist_elem = soup.select(
                'article[class="song-info"] div[class="details"] br'
            )
            for index,track_elem in enumerate(tracklist_elem):
                try:
                    track = ''.join(track_elem.previous_sibling).strip('\r\n')
                except:
                    continue
                track_list.append(track)
            return dict(type='album',category=category,artist=artist, title=title, category_art=art_link, category_download=download_link, category_tracks_details=track_list)
        head = header_elem.text.split("] ")[1].split(" – ")
        artist,title = head if len(head) is 2 else header_elem.text.split("] ")[1].split(" - ")
        return dict(type='track',category=category,artist=artist, title=title, category_art=art_link, category_download=download_link)
