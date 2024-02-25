import asyncio, time
import re
from engine.version2.root import BaseEngine
from tqdm import tqdm
from itertools import repeat


class SongsLover(BaseEngine):
    name = "Songslover"
    summary = "SongsLover is a website that both search and fetch songs"
    categories = (
        'albums','tracks',
        'best-of-the-month','mixtapes',
        'music-albums'
    )

    def __init__(self):
        super().__init__()
        self.site_uri = "https://songslover.me/"
        self.request_method = self.GET
       
    async def fetch(self, category="tracks", page=1, **kwargs):
        # Parse Uri
        url = self.get_formated_url(url=kwargs.pop('url'),path="",params='') if kwargs 
        else self.get_formated_url(category=category,page=page,params={},**kwargs)
        
        # Get Page containing tracks
        soup = self.get_response_object(url)

        # Extract track links from page
        track_list = [elem['href'] for elem in soup.select("article h2 a")]

        # extract each detail for each track asynchronously
        result = asycnio.gather(
                )

        with ProcessPoolExecutor() as executor:
            result = executor.map(self.custom_parser, track_list, repeat(category))
 
        return [elem for elem in result]



