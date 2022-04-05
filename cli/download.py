import shutil
import tempfile
import requests
import os
from utils import helpers
from utils.cache import Cache


TEMP_DIR = tempfile.gettempdir()
NAME = os.path.basename(__file__)[:-3]
CACHE = Cache(os.path.dirname(os.path.abspath(__file__)))

def download_file(uri, referer=None):
    """Download Mp3 Files Into Temp Dir"""
    temp_name,cache_hit = CACHE.retrieve(NAME,uri,TEMP_DIR)
    #check cache hit
    if cache_hit:
       return temp_name 

    #fetch from web   
    headers = helpers.get_header()
    headers['referer'] = referer if referer is not None else ''
    temp = tempfile.NamedTemporaryFile(delete=False, dir=TEMP_DIR)
    with requests.get(uri, headers=headers, stream=True) as r:
        with open(temp.name, "wb") as f:
            shutil.copyfileobj(r.raw, f) 
    temp_name,cache_hit = CACHE.put_update(NAME,uri,temp.name)
    return temp_name
   
