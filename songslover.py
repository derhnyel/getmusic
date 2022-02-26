from root import RootFetch
from lxml import etree


class Fetch(RootFetch):
    engine_name = "Songslover"
    page_path = "page"
    tracks_category = "category"

    def __init__(self):
        super().__init__()
        self.site_uri  = "https://songslover.vip/"

    def get_url_path(self,page=None,type_=None):       
        return (type_,self.page_path,page) if type_=="albums" else (self.tracks_category,type_,self.page_path,page)

    def parse_parent_soap(soup):
        result = [] #use enum/dict object generator
        soup_elements = soup.select('article h2')
        for element in soup_elements:
            temp_result = {}
            try:
                artist,title=element.text.split(' –')
            except: 
                title = artist = element.text
            artist = artist.strip()
            title = title.strip()     
            link = element.a['href']
            temp_result['artist']=artist 
            temp_result['title']=title
            temp_result['link']= link
            result.append(temp_result)
        return result
    def parse_child_soup(soup):
        dom = etree.HTML(str(soup))        

    
    
