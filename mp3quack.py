from root import RootFetch


class Fetch(RootFetch):
    engine_name = 'mp3quack'
    mp3_path ='mp3'

    def __init__(self):
        super().__init__()
        self.site_uri  = 'https://mp3-juice.com/'
        self.request_method = self.GET
        self.reponse_type = self.HTML
    

    def get_url_path(self):
        return (self.mp3_path)

    def parse_child_object(object):    
        """Parse JSON OBJECT To extract download_links,arts,and song_titles"""
        return    