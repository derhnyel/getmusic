import shutil
import tempfile
import requests
from utils import helpers
import concurrent.futures

AUDIUS_API_ENDPOINT = "https://api.audius.co"

TEMP_DIR = tempfile.gettempdir()


def make_uri(path):
    api_endpoint = get_api_endpoint()
    uri = f"{api_endpoint}/v1/{path}"
    return uri


def download_file(uri):
    temp = tempfile.NamedTemporaryFile(delete=False, dir=TEMP_DIR)
    with requests.get(uri, stream=True) as r:
        with open(temp.name, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return temp.name


def get_redirect_uri(uri):
    r = requests.head(uri, allow_redirects=True)
    return r.url


def get(path, payload={}):
    #request_method =self.GET

    #get queryparams
    payload["app_name"] = "audius-cli"
    
    #get formated url
    #path changes so you format paths
    uri = make_uri(path)

    #get response object
    r = requests.get(uri, params=payload)
    
    #Move to search method
    #body = r.json()
    #if not r.ok:  # not 2xx
    #    return None
    #return body.get("data", [])

    def get_query_params(self, query=None,page=None,category=None,default=None,**kwargs,):
        if default is not None:
           default["app_name"]="audius-cli"
           return default   
        return {
                "app_name":"audius-cli"
            }    


#search method allows search by tracks,users and playlists
#category=tracks,users,playlists
def search_entity(entity_type):
    def search(query):
        search_params = {"query": query}
        path = f"{entity_type}/search"
        return get(path, search_params)

    return search


#create this function new
#use the get response object(siteurl=audiusapiendpoint,)
#call get formated url(url=get_api_endpoint,path={'v1',category})
def get_api_endpoint():
    r = requests.get(AUDIUS_API_ENDPOINT)
    body = r.json()
    endpoints = body["data"]
    return helpers.get_random_element_from_list(endpoints)

#search by artist and track


#fetch by playlist

#allowed_categories = (tracks,favourites,reposts,trending)


#fetch methods by user_id and playlist_id
def get_playlist_tracks(playlist_id):
    path = f"playlists/{playlist_id}/tracks"
    return get(path)


def get_user_tracks(user_id):
    path = f"users/{user_id}/tracks"
    return get(path)


def get_favorite_tracks(user_id):
    path = f"/users/{user_id}/favorites"
    favorite_pointers = get(path)
    favorite_track_ids = [
        fav["favorite_item_id"]
        for fav in favorite_pointers
        if fav["favorite_type"] == "SaveType.track"
    ]
    favs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        track_fetch_futures = {
            executor.submit(get, f"tracks/{id}"): id for id in favorite_track_ids
        }
        for future in concurrent.futures.as_completed(track_fetch_futures, timeout=30):
            result = future.result()
            favs.append(result)

    return [fav for fav in favs if fav]


def get_reposted_tracks(user_id):
    path = f"/users/{user_id}/reposts"
    all_reposts = get(path)
    track_reposts = [
        repost["item"] for repost in all_reposts if repost["item_type"] == "track"
    ]
    return track_reposts


def get_trending():
    path = "tracks/trending"
    return get(path)



########################################################################################################################
# headers = {
#   'Accept': 'application/json'
# }

# _____________________flow for search ________________________
# if category = users/artist
# api end point to getuser with search query
# get request to response = requests.get('https://discovery-a.mainnet.audius.coresci.tech/v1/users/search', params={'query': 'Brownies',  'app_name': 'getmusic'}, headers = headers)
# user_ids = ((user.get('id),user.get('name') for user in response['data'])
# get all tracks under that user
# response = requests.get('https://discovery-a.mainnet.audius.coresci.tech/v1/users/{user_id}/tracks', params={'app_name': 'getmusic'}, headers = headers)
# .json get response['data'] and loop through
# dict(
# type='track'  
# category=category    
# artist=name
# genre=genre
# title = title
# mood = mood
# art = artwork
# download = #calldownloadfunction and pass it track id to format the track
# duration = duration/60
# )
#if category == tracks
# search tracks
#r = requests.get('https://discovery-a.mainnet.audius.coresci.tech/v1/tracks/search', params={'query': 'baauer b2b',  'app_name': 'EXAMPLEAPP'}, headers = headers)
#get response['data'] and loop through
#--Parse single Function
# dict(
# type='track'  
# category=category    
# artist=name
# genre=genre
# title = title
# mood = mood
# art = artwork
# download = #calldownloadfunction and pass it track id to format the track
# duration = duration/60
# )



#_______________FETCH_____________
#if category is trending
#r = requests.get('https://discovery-a.mainnet.audius.coresci.tech/v1/tracks/trending', params={'app_name': 'EXAMPLEAPP'}, headers = headers)
#loop through and call parse single objects

#if category=playlist