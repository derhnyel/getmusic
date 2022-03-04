from root import RootFetch
import re
#from lxml import etree


class Fetch(RootFetch):
    engine_name = 'songslover'
    page_path = 'page'
    tracks_category = 'category'

    def __init__(self):
        super().__init__()
        self.site_uri  = 'https://songslover.vip/'
        self.request_method = self.GET
        self.reponse_type = self.HTML

    """Implement to """
    def get_url_path(self,page=None,category=None):
        if page <= 0 or page is None:
            page = 1
        if page >= 251:
            page = 250     
        return (category,self.page_path,page) if category=='albums' else (self.tracks_category,category,self.page_path,page)
    
    
    def parse_parent(soup,**kwargs):
        return list(elem['href'] for elem in soup.select('article h2 a'))    
    
    def parse_child_object(soup,category=None,**kwargs):
        try:
            artist,title = soup.select('div[class="post-inner"] h1 span[itemprop="name"]')[0].text.split(' –')
            artist,title = artist.strip(),title.strip() 
        except Exception:
            artist = title = soup.select('div[class="post-inner"] h1 span[itemprop="name"]')[0].text        
        try:
            art_link = soup.select('div[class="entry"] img[src]')[0]['src']
        except Exception:
            art_link = None
        if category=="albums":
            try:
                download_link = soup.find(text = re.compile(".*(All).*(in).*(One).*(Server).*(2).*")).find_previous("a")['href']
            except Exception:
                download_link = None
            response_group = [
            soup.select('li strong a'),soup.select('p span strong a'),
            soup.select('tr td div[class="wpmd"] a'),soup.select('span[style="color: #99cc00;"] a'),
            soup.select('span[style="color: #ff99cc;"] a'),
            ]
            valid_group = list(i for i in response_group if i!=[])
            if len(valid_group)<=0:
                return None
            response_elements = valid_group[0]
            for element in response_elements:
                try:
                    song_title = element.text
                    if song_title is None:
                        continue
                    song_link = element['href']
                    keywords = [
                        'Server','Youtube',
                        'Apple Store','Apple Music','ITunes',
                        'Amazon Music','Amazon Store',
                        'Buy Album','Download Album',
                        ]
                    keyword = [i for i in keywords if i in song_title]
                    if any(keyword) :
                        continue
                    elif song_title.startswith('Download'):
                        song_title = song_title[8:] 
                except Exception:
                    pass
            return    
        regex_group = [
            soup.find(text = re.compile('.*(Save).*(Link)$')),soup.find(text = re.compile('.*(Save).*(Link).*(Server){1}.*(2){1}$')),
            soup.find(text = re.compile('.*(Download)$')),soup.find(text = re.compile('.*(Download).*(This){1}.*(Track){1}$')),
            soup.find(text = re.compile('.*(Save).*(File)$')),
        ]
        valid_group = list(i for i in regex_group if i!=None)
        if len(valid_group) >= 1:
            download_link = valid_group[0].find_previous('a')['href']
        download_link = None
        return    






    
    
