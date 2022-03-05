from root import RootSearch
"""Figure out a way to combine both ftch and search"""
"""Also find a way to differentiate between album and track children when using Search not Fetch"""

class Fetch(RootSearch):
    engine_name = 'justnaija'
    page_path='page'
    album_path = 'album'
    album_category='music'
    tracks_page_path = 'music-mp3'

    def __init__(self):
        super().__init__()
        self.site_uri = 'https://justnaija.com/'
        self.request_method= self.GET
        self.response_type = self.HTML

    def get_url_path(self,page=None,category=None):
        #if page
        return  (self.tracks_page_path,self.page_path,page) if category==self.TRACK else (self.album_category,self.album_path,self.page_path,page)  
    

    def parse_parent_object(self,soup):
        return list(elem['href'] for elem in soup.select("main article h3 a"))


    def parse_object(self,soup,category=None):
        header_elem = soup.select('div[class="mpostheader"] span[class="h1"]')[0]
        try:
            download_link = soup.select('p[class="song-download"] a')[0]['href']
        except Exception:
            download_link = None        
        art_link= soup.select('figure[class="song-thumbnail"] img')[0]['src']
        if category == self.TRACK:    
            artist,title = header_elem.text.split("] ")[1].split(" – ") 
            return 
        artist,title = header_elem.text.split(" | ")[0].split(" – ")
        tracklist_elem = soup.select('div[class="mu-o-c"] div[class="mu-o-unit-c"] div[class="album-side-1"]')
        for track_elem in tracklist_elem:
            song_link = track_elem.h4.a['href']
            song_title = track_elem.h4.a.text + track_elem.span.text if track_elem.span!=None else track_elem.h4.a.text 
        return

    def fetch(self,page=None,category=None,**kwargs):
        self.search(page=page,category=category,**kwargs)


class Search(Fetch):
    def __init__(self):
        super().__init__()