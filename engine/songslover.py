import re
from engine.root import BaseEngine
from tqdm import tqdm

class SongsLover(BaseEngine):
    
    engine_name = "Songslover"
    summary = None #Get Summary

    allowed_categories = ('albums','tracks','best-of-the-month','mixtapes','music-albums')
    
    def __init__(self):
        super().__init__()
        self.site_uri = "https://songslover.me/"
        self.request_method = self.GET

    def fetch(self,category='tracks',page=1,**kwargs):

        """Fetch Latest Items Based on Category and Page Number"""
        
        # Allows a url too
        soup = self.get_response_object(
            url = self.get_formated_url(url=kwargs.pop('url'),path='',params='') if kwargs.get(
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
                self.get_response_object(elem["href"], **kwargs),
                category=elem['href'].split('/')[3],
                **kwargs)
            for elem in tqdm(soup.select("article h2 a"))
        )

    def parse_single_object(self, soup, category=None, **kwargs):
        """
        Parses the source code to return

        :param : soup: link found in <article h2 a>
        :type soup: `bs4.element.ResultSet`
        :param : category: album or track 
        :type category: `str`
        :return: parsed title, download_link ,category of soup
        :rtype: dict
        """
        
        ##### Developer Note #####
        # Songslover has upgraded thier pages multiple times so the page elements are different
        # This is parsed to accomadate some of the changes 

        # Extract artist and song title. art and download_link
        artist, title = self._get_description(soup)
        art_link = self._get_art_link(soup)
        download_link = self._get_download_link(soup, category)
        
        # different way to retrieve information from Album soups and single track Soups    
        if category == "tracks":
            if download_link!=None:
                return dict(type='track',category=category,artist=artist,title=title,
                    download=download_link,art=art_link)
            
        # Get song and individual download link for song
        else:
            track_details = self._get_individual_download_link(soup)
            return dict(type='album',category=category,artist=artist,title=title,
                download=download_link,art=art_link,details=track_details)
    
    
    def get_query_params(self, query=None,**kwargs):
        return {
            's':query
        }

    def get_url_path(self, page=None, category=None):
        """Path to Page Content"""
        if page <= 0:
            page = 1
        if page >= 256:
            page = 255
        return (category, self.page_path, str(page)) 
    
    def _get_description(self, soup):
        description = soup.select(
            'div[class="post-inner"] h1 span[itemprop="name"]'
        )[0].text.strip().split("–")
        if len(description) == 2:
            artist, title = description
        else:
            # track_type: could be an EP single
            artist,title,_ = description
            
        return artist, title
    
    def _get_art_link(self, soup):
        """Generate the art link of a song

        Args:
            img_tag (: bs4.element.Tag): Image element contain art links with different sizes
        """
        try:
            art_link = soup.select('div[class="entry"] img[src]')[0]["data-src"]
        except Exception:
            art_link = None
        return art_link
        
    def _get_download_link(self,soup, category):
        download_link = None
        if category == "track":
            # Handle different Formats to Get Download Link
            regex_group = [
                soup.find(text=re.compile(".*(Save).*(Link)$")),
                soup.find(text=re.compile(".*(Save).*(Link).*(Server){1}.*(2){1}$")),
                soup.find(text=re.compile(".*(Download)$")),
                soup.find(text=re.compile(".*(Download).*(This){1}.*(Track){1}$")),
                soup.find(text=re.compile(".*(Save).*(File)$")),
            ]
            valid_group = list(i for i in regex_group if i != None)
            if len(valid_group) >= 1:
                try:
                    # check for a previous link
                    download_link = valid_group[0].find_previous("a")["href"]
                except KeyError:
                    # check for a next link
                    try:
                        download_link = valid_group[0].find_next("a")["href"]        
                    except KeyError:
                        pass
        else:            
            valid_group = [
                soup.find(text=re.compile(".*(All).*(in).*(One).*(Server).*(2).*")),
                soup.find(text=re.compile(".*(All).*(One)"))
            ]
            valid_group = [elem for elem in valid_group if elem is not None]
            if len(valid_group) >= 1:
                try:
                    # check for a previous link
                    download_link = valid_group[0].find_previous("a")["href"]
                except KeyError:
                    # check for a next link
                    try:
                        download_link = valid_group[0].find_next("a")["href"]
                    except:
                        pass
        
        return download_link
     
    def _get_individual_download_link(self, soup):
        
        keywords = ["Server","Youtube","Apple Store","Apple Music",
            "ITunes","Amazon Music","Amazon Store","Buy Album","Download Album",]
        
        response_group = [
            # soup.select('div[id="main-content"] div[class="post-inner"] div[class="entry"] ol li'),
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
            
            # Skip song if title or link isn't avaible
            song_title = element.text
            if song_title is None:
                continue
            try:
                song_link = element["href"]
            except KeyError:
                continue
            
            # Remove Certain title's with these keywords from result
            keyword = [i for i in keywords if i in song_title]
            if any(keyword):
                continue

            # Some elements Have 'Download' appended before the song Title
            # elif song_title.startswith("Download"):
            #     song_title = song_title[8:]
            tracks_details.append(dict(title=song_title,download_link=song_link)) 

        return tracks_details