import shutil
import tempfile
import requests
from utils import helpers

TEMP_DIR = tempfile.gettempdir()


def download_file(uri, referer=None):
    headers = helpers.get_header()
    headers['referer'] = referer if referer is not None else ''
    temp = tempfile.NamedTemporaryFile(delete=False, dir=TEMP_DIR)
    with requests.get(uri, headers=headers, stream=True) as r:
        with open(temp.name, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return temp.name

#####Implement a cache each temp file should be cached    
