
#https://justnaija.com/music/album/page/1-19
#https://justnaija.com/music-mp3/1-286
import requests
from bs4 import BeautifulSoup as bs4 
from fake_useragent import UserAgent
import time



UAgent = UserAgent()
mode = None



def func(link):
    time.sleep(0.1)
    resp= requests.get(link,headers={"User-Agent": UAgent.random})
    sss = bs4(resp.text,"html.parser")
    pg = sss.select('div[class="mu-o-c"] div[class="mu-o-unit-c"] div[class="album-side-1"]')
    #download_link for both tracks and albums
    try:
        download_link = sss.select('p[class="song-download"] a')[0]['href']
    except:
        download_link =None    
    print("Album Download Link : " ,download_link)
    cnt=1
    for i in pg:
        song_link = i.h4.a['href']
        song_title = i.h4.a.text + i.span.text if i.span!=None else i.h4.a.text
        print("---TRACK "+str(cnt)+"--- "+song_title)
        cnt+=1
  
for i in range(16,20):
    print('_______________________________PAGE ' + str(i)+'_________________________________________')
    uri = "https://justnaija.com/music/album/page/"+str(i)
    webpage = requests.get(uri,headers={"User-Agent": UAgent.random})


    ssp = bs4(webpage.content, "html.parser")
    jt = ssp.select("main article aside a")
    jp = ssp.select("main article h3 a")
    jimg = ssp.select("main article img")
    for index in range(len(jp)):
            title=jp[index].text
            link=jp[index]['href']
            artist=jt[index].text
            art_link=jimg[index]['data-src']
            print("Artist Name: ",artist)
            print('Album Title : ',title)
            print("Album Art :" ,art_link)
            func(link)

####Tracks
        #artist,title=jp[index].text.split("–")





 
       

