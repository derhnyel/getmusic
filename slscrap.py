#import fake
import time
from lxml import etree
import requests
from bs4 import BeautifulSoup as bs4 
from fake_useragent import UserAgent

UAgent = UserAgent()
mode = None
#uri="https://songslover.vip/"
#url_albums = "https://songslover.vip/albums/page/1-303"
#url_tracks = "https://songslover.vip/category/tracks/page/1-388"
#song_db_album={'artist_name':{'title':[art_link,download_link,[('song_title','song_link')]]}}
#song_db_track={'artist_name':{'title':[art_link,download_link]}}


def fetch_details(uri,track=False):
    global mode
    webpage = requests.get(uri,headers={"User-Agent": UAgent.random})
    soup = bs4(webpage.content, "html.parser")
    soup_elements = soup.select('article h2')
    for element in soup_elements:
        try:
            artist_name,title=element.text.split(' –')
        except:
            continue  
        artist_name=artist_name.strip()
        title=title.strip()     
        url = element.a['href']
        #(artist_name,title,url)
        print(artist_name,title)
        if track:
            mode = 'track'
            song_details= get_tracks(url)
            #song_db_track[artist_name]={title:[song_details[0],song_details[1]]} 
            #song_db_track[artist_name]={title:[art_link,download_link]} 
        else:
            mode = 'album'
            song_details = get_tracks(url)
            #song_db_album[artist_name]={title:[song_details[0],song_details[1],songs_details[2]]}  
            #song_db_album[artist_name]={title:[art_link,download_link,songs_collection]}  
            

def get_tracks(url):
    time.sleep(0.1) 
    response = requests.get(url, headers={"User-Agent": UAgent.random})
    response_soup=bs4(response.text,"html.parser")
    dom = etree.HTML(str(response_soup))
    try:
        art_link=response_soup.figure.img['src']
    except:
        try:
            art_link= response_soup.select('div[class="entry"] p')[0].img['src']
        except:
            art_link= response_soup.select('div[class="entry"] h2')[0].img['src']    

    if mode == "track":
        try:
            download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[3]/strong/a/@href')[0]
        except:
            try:
                download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[2]/span/a/@href')[0] 
            except:
                try:
                    download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[2]/span/strong/a/@href')[0] 
                except:
                    try:
                        download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[2]/strong/a/@href')[0]
                    except:
                        try:
                            download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/h2/span/a/@href')[0] 
                        except:
                            download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[2]/a/@href')[0] 

        if download_link.endswith(".htm") or download_link.endswith(".html"):  
            return None             
        return art_link,download_link
    else:
        #//*[@id="the-post"]/div/div[2]/p[6]/strong/a
        download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[5]/strong/a/@href')[0]
        if download_link.endswith(".htm") or download_link.endswith(".html") :
            download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[6]/strong/a/@href')[0]
    print(download_link)         
    response_elements = response_soup.select('li strong')
    songs_collection=[]
    for element in response_elements:
        try:
            song_link = element.a['href']
            song_title = element.a.text
            songs_collection.append((song_title,song_link))
        except:
            pass
            #song_title=j.text
            #temp_songs_dict.append((song_title,"@#$%@^!"))      
    return art_link,download_link,songs_collection,      

#for i in range(5,5):
#    print('Page : '+str(i))
url_albums = "https://songslover.vip/albums/page/250"
fetch_details(url_albums)
