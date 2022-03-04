from root import RootFetch


class Fetch(RootFetch):
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
        return (self.album_category,self.album_path,self.page_path,page) if category=="albums" else (self.tracks_page_path,self.page_path,page)    
    

    def parse_parent(soup):
        return list(elem['href'] for elem in soup.select("main article h3 a"))


    def parse_child_result(soup,category=None):
        header_elem = soup.select('div[class="mpostheader"] span[class="h1"]')[0]
        try:
            download_link = soup.select('p[class="song-download"] a')[0]['href']
        except Exception:
            download_link = None        
        art_link= soup.select('figure[class="song-thumbnail"] img')[0]['src']
        if category == "albums":    
            artist,title = header_elem.text.split(" | ")[0].split(" – ")
            tracklist_elem = soup.select('div[class="mu-o-c"] div[class="mu-o-unit-c"] div[class="album-side-1"]')
            for track_elem in tracklist_elem:
                song_link = track_elem.h4.a['href']
                song_title = track_elem.h4.a.text + track_elem.span.text if track_elem.span!=None else track_elem.h4.a.text 
            return
        artist,title = header_elem.text.split("] ")[1].split(" – ") 
        return          