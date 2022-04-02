import re
from engine.root import BaseEngine

class SongsLover(BaseEngine):
    
    engine_name = "Songslover"
    summary = None #Get Summary

    allowed_categories = ('albums','tracks','best-of-the-month','mixtapes','music-albums')
    
    def __init__(self):
        super().__init__()
        self.site_uri = "https://songslover.vip/"
        self.request_method = self.GET

    def fetch(self,category='tracks',page=1,**kwargs):

        """Fetch Latest Items Based on Category and Page Number"""
        # Allows a url too
        soup = self.get_response_object(url = self.get_formated_url(url=kwargs.pop('url'),path='',params='') if kwargs.get(
            'url') else self.get_formated_url(category=category, page=page, params={},**kwargs)) 
        self.results=self.parse_parent_object(soup,**kwargs)
        return self.results

    def search(self,query='',page=1,category=None,**kwargs):
        """Search Engine with query, page ,category parameters"""

        # Either search through url or search through query
        search_url = self.get_formated_url(url=kwargs.pop('url'),path='',params='' ) if kwargs.get(
            #get the formated urls
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
        
    
        
    def parse_parent_object(self, soup,**kwargs):
        """
        Parses Engine Soup for links to individual items 
        and parse those links then pass thier soups to parse single object
        """
        return list(
            self.parse_single_object(
                self.get_response_object(elem["href"],**kwargs),
                category=elem['href'].split('/')[3],
                **kwargs)
            for elem in soup.select("article h2 a")
        )

    def parse_single_object(self,soup, category=None, **kwargs):
        """
        Parses the source code to return

        :param : soup: link found in <article h2 a>
        :type soup: `bs4.element.ResultSet`
        :param : category: album or track 
        :type category: `str`
        :return: parsed title, download_link ,category of soup
        :rtype: dict
        """
        # Songslover has upgraded thier pages multiple times so the page elements are different
        # THis is parsed to accomadate some of the changes 

        # Some div contain title and Artist while some do not
        try:
            artist, title = soup.select(
                'div[class="post-inner"] h1 span[itemprop="name"]'
            )[0].text.split(" –")
            artist, title = artist.strip(), title.strip()    
        except Exception:
            artist = title = soup.select(
                'div[class="post-inner"] h1 span[itemprop="name"]'
            )[0].text

        #Some Soups do not have art links    
        try:
            art_link = soup.select('div[class="entry"] img[src]')[0]["src"]
        except Exception:
            art_link = None

        #different way to retrieve information from Album soups and single track Soups    
        if category == "tracks":
            #HAndle different Formats to Get Download Link
            regex_group = [
                soup.find(text=re.compile(".*(Save).*(Link)$")),
                soup.find(text=re.compile(".*(Save).*(Link).*(Server){1}.*(2){1}$")),
                soup.find(text=re.compile(".*(Download)$")),
                soup.find(text=re.compile(".*(Download).*(This){1}.*(Track){1}$")),
                soup.find(text=re.compile(".*(Save).*(File)$")),
            ]
            valid_group = list(i for i in regex_group if i != None)
            download_link = valid_group[0].find_previous("a")["href"] if len(valid_group) >= 1 else None
            if download_link!=None:
                return dict(type='track',category=category,artist=artist,title=title,download=download_link,art=art_link,details=(title,download_link))
        
        #For category other than tracks
        try:
            download_link = soup.find(
                text=re.compile(".*(All).*(in).*(One).*(Server).*(2).*")
            ).find_previous("a")["href"]
        except Exception:
            download_link = None
        # Get soup element to extract Song title and Song links for albums   
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
                # Remove Certain title's with these keywords from result
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
                # Some elements HAve 'Download' appended before the song Title
                elif song_title.startswith("Download"):
                    song_title = song_title[8:]
                tracks_details.append((song_title,song_link))    
            except Exception:
                pass
        return dict(type='album',category=category,artist=artist,title=title,download=download_link,art=art_link,details=tracks_details)
    
    
    def get_query_params(self, query=None,**kwargs):
        return {
            's':query
        }

    def get_url_path(self, page=None, category=None):
        """PAth to Page Content"""
        if page <= 0:
            page = 1
        if page >= 256:
            page = 255
        return (category, self.page_path, str(page)) 