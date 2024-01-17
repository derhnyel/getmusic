import subprocess
from utils import helpers
import shutil
import tempfile
import requests
from playsound import playsound



TEMP_DIR = tempfile.gettempdir()
##stream/ download audio files
def stream(download_uri,referer=None):
    local_filepath = download_file(download_uri,referer=referer)
    # stop()
    #subprocess.Popen(["afplay", local_filepath])
    playsound(local_filepath)

def stop():
    subprocess.call(
        ["killall", "afplay"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )

def download_file(uri,referer=None):
    headers = helpers.get_header()
    headers['referer'] = referer if referer is not None else '' 
    temp = tempfile.NamedTemporaryFile(delete=False, dir=TEMP_DIR)
    with requests.get(uri,headers=headers,stream=True) as r:
        with open(temp.name, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return temp.name    