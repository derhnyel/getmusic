import re
from engine.root import BaseEngine

# from lxml import etree

"""Figure out a way to combine both fetch and search"""
"""Also find a way to differentiate between album and track children when using Search not Fetch"""

class SongsLover(BaseEngine):
    #create_Enum
    engine_name = "songslover"
    page_path = "page"

    allowed_categories = ('albums','tracks','best-of-the-month','mixtapes','music-albums')

    def __init__(self):
        super().__init__()
        self.site_uri = "https://songslover.vip/"
        self.request_method = self.GET

    def fetch(self,category='tracks',page=1,**kwargs):
        #update Formated url
        soup = self.get_response_object(url = self.get_formated_url(url=kwargs.pop('url'),path='',params='') if kwargs.get(
            'url') else self.get_formated_url(category=category, page=page, params={},**kwargs)) 
        self.results=self.parse_parent_object(soup,**kwargs)
        return self.results
        
    def get_url_path(self, page=None, category=None):
        if page <= 0:
            page = 1
        if page >= 256:
            page = 255
        return (category, self.page_path, str(page)) 
        
    def parse_parent_object(self, soup,**kwargs):
        return list(
            self.parse_single_object(self.get_response_object(elem["href"],**kwargs),category=elem['href'].split('/')[3],**kwargs)
            for elem in soup.select("article h2 a")
        )

    def search(self,query=None,page=1,category=None,**kwargs):
        search_url = self.get_formated_url(url=kwargs.pop('url'),path='',params='' ) if kwargs.get(
            'url') else self.get_formated_url(
            query = query,
            path = (
                self.page_path,str(page)),
                page=page,
                category=category,
                **kwargs,
                )     
        soup = self.get_response_object(url=search_url,**kwargs)
        self.results = self.parse_parent_object(soup,**kwargs)
        return self.results

    def get_query_params(self, query=None,**kwargs):
        return {
            's':query
        }

    def parse_single_object(self,soup, category=None, **kwargs):
        try:
            artist, title = soup.select(
                'div[class="post-inner"] h1 span[itemprop="name"]'
            )[0].text.split(" –")
            artist, title = artist.strip(), title.strip()
        except Exception:
            artist = title = soup.select(
                'div[class="post-inner"] h1 span[itemprop="name"]'
            )[0].text
        try:
            art_link = soup.select('div[class="entry"] img[src]')[0]["src"]
        except Exception:
            art_link = None
        if category == "tracks":
            regex_group = [
                soup.find(text=re.compile(".*(Save).*(Link)$")),
                soup.find(text=re.compile(".*(Save).*(Link).*(Server){1}.*(2){1}$")),
                soup.find(text=re.compile(".*(Download)$")),
                soup.find(text=re.compile(".*(Download).*(This){1}.*(Track){1}$")),
                soup.find(text=re.compile(".*(Save).*(File)$")),
            ]
            valid_group = list(i for i in regex_group if i != None)
            download_link = valid_group[0].find_previous("a")["href"] if len(valid_group) >= 1 else None
            return dict(type='track',category=category,artist=artist,title=title,category_download=download_link,category_art=art_link)

        try:
            download_link = soup.find(
                text=re.compile(".*(All).*(in).*(One).*(Server).*(2).*")
            ).find_previous("a")["href"]
        except Exception:
            download_link = None
        response_group = [
            soup.select("li strong a"),
            soup.select("p span strong a"),
            soup.select('tr td div[class="wpmd"] a'),
            soup.select('span[style="color: #99cc00;"] a'),
            soup.select('span[style="color: #ff99cc;"] a'),
        ]
        valid_group = list(i for i in response_group if i != [])
        if len(valid_group) <= 0:
            return None
        response_elements = valid_group[0]
        tracks_details = []
        for element in response_elements:
            try:
                song_title = element.text
                if song_title is None:
                    continue
                song_link = element["href"]
                keywords = [
                    "Server",
                    "Youtube",
                    "Apple Store",
                    "Apple Music",
                    "ITunes",
                    "Amazon Music",
                    "Amazon Store",
                    "Buy Album",
                    "Download Album",
                ]
                keyword = [i for i in keywords if i in song_title]
                if any(keyword):
                    continue
                elif song_title.startswith("Download"):
                    song_title = song_title[8:]
                tracks_details.append((song_title,song_link))    
            except Exception:
                pass
        return dict(type='album',category=category,artist=artist,title=title,category_download=download_link,category_art=art_link,category_tracks_details=tracks_details)
