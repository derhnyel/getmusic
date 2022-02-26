from root import RootFetch
from lxml import etree


class Fetch(RootFetch):
    engine_name = "Songslover"
    page_path = "page"
    tracks_category = "category"

    def __init__(self):
        super().__init__()
        self.site_uri  = "https://songslover.vip/"

    def get_url_path(self,page=None,format=None):       
        return (format,self.page_path,page) if format=="albums" else (self.tracks_category,format,self.page_path,page)

    def parse_parent_soap(soup):
        return list(elem['href'] for elem in soup.select('article h2 a'))
    
    
    
    def parse_child_soup(soup,format=None):
        dom = etree.HTML(str(soup))
        try:
            artist,title = soup.select('div[class="post-inner"] h1 span[itemprop="name"]').text.split(' –')
            artist,title = artist.strip(),title.strip() 
        except:
             artist=title=soup.select('div[class="post-inner"] h1 span[itemprop="name"]').text        
        art_link = soup.select('div[class="entry"] img[src]')[0]['src']        

    
    
