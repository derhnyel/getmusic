import time
from lxml import etree
import requests
from bs4 import BeautifulSoup as bs4 
from fake_useragent import UserAgent
import re

UAgent = UserAgent()
mode = None
#uri="https://songslover.vip/"
#url_albums = "https://songslover.vip/albums/page/1-303"
#url_tracks = "https://songslover.vip/category/tracks/page/1-388"
#song_db_album={'artist_name':{'title':[art_link,download_link,[('song_title','song_link')]]}}
#song_db_track={'artist_name':{'title':[art_link,download_link]}}

# BUILD AN ENGINE FOR SONGSLOVER SCRAPPER
def fetch_details(uri,track=False):
    global mode
    webpage = requests.get(uri,headers={"User-Agent": UAgent.random})
    soup = bs4(webpage.content, "html.parser")
    soup_elements = soup.select('article h2')
    for element in soup_elements:
        # try:
        #     artist_name,title=element.text.split(' –')
        # except: 
        #     title = artist_name = element.text
        # artist_name=artist_name.strip()
        # title = title.strip()     
        url = element.a['href']
        #(artist_name,title,url)
        #print("Artist Name: %s , Album/Track Title: %s"%(artist_name,title))
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
    #time.sleep(0.1) 
    response = requests.get(url, headers={"User-Agent": UAgent.random})
    response_soup=bs4(response.text,"html.parser")
    #dom = etree.HTML(str(response_soup))
    try:
        artist,title = response_soup.select('div[class="post-inner"] h1 span[itemprop="name"]')[0].text.split(' –')
        artist,title = artist.strip(),title.strip() 
    except Exception:
        artist=title=response_soup.select('div[class="post-inner"] h1 span[itemprop="name"]')[0].text        
    try:
        art_link = response_soup.select('div[class="entry"] img[src]')[0]['src']
    except:
        art_link=None    
    print("Artist Name: %s , Album/Track Title: %s"%(artist,title))
    #REFACTOR LINE 48-57
    # try:
    #     art_link=response_soup.figure.img['src']
    # except:
    #     try:
    #         art_link= response_soup.select('div[class="entry"] p img[src]')[0]['src']
    #     except:
    #         try:
    #             art_link= response_soup.select('div[class="entry"] h2 img[src]')[0]['src']
    #         except:
    #             return None        
    #REFACTOR LINE 58 - 83
    if mode == "track":
        #USE REGEX TO SEARCH 
        #"Download,Save Link, Save Link Server 2,Download This Track ---- page 295"
        #re.compile(r'(.*(Save).*(Link).*(Server){,1}.*(2){,1}.*)*(.*(Download).*(This){,1}.*(Track){,1}.*)')
        regex_group = [

            response_soup.find(text = re.compile('.*(Save).*(Link)$')),
            response_soup.find(text = re.compile('.*(Save).*(Link).*(Server){1}.*(2){1}$')),
            response_soup.find(text = re.compile('.*(Download)$')),
            response_soup.find(text = re.compile('.*(Download).*(This){1}.*(Track){1}$')),
            response_soup.find(text = re.compile('.*(Save).*(File)$')),

        ]
        #,response_soup.find(text = re.compile('.*(Save).*(File).*(Server){1}.*(2){1}$')))
        valid_group = list(i for i in regex_group if i!=None)
        if len(valid_group)>=1:
            download_link = valid_group[0].find_previous('a')['href']
        else:
            download_link = None    
        # print(check)
        # if any(check):
            #index = check.index(True)
            #download_link = reg[index].find_previous('a')['href']
        # else:
            #download_link = None    


        #download_link = response_soup.find_all(text = re.compile('.*(Save).*(Link).*(Server){,1}.*(2){,1}.*')).find_previous('a')['href']
        # try:
        #     download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[3]/strong/a/@href')[0]
        # except:
        #     try:
        #         download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[2]/span/a/@href')[0] 
        #     except:
        #         try:
        #             download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[2]/span/strong/a/@href')[0] 
        #         except:
        #             try:
        #                 download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[2]/strong/a/@href')[0]
        #             except:
        #                 try:
        #                     download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/h2/span/a/@href')[0] 
        #                 except:
        #                     try:
        #                         download_link = response_soup.find(string= "Save Link").find_previous('a')['href']
        #                     except:
        #                         download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[2]/a/@href')[0] 
        print("Track Art : " ,art_link)
        print("Track Download Link : " ,download_link)
        # if download_link.endswith(".htm") or download_link.endswith(".html"):  
        #     return None                 
        return art_link,download_link
    #REFACTOR ....TOO MANY TRY / EXCEPTS LINE 84-113 ______USE A REGEX TO Check For WORD LIKE [All,in,One,Server,2]
    else:
        try:
            download_link = response_soup.find(text = re.compile(".*(All).*(in).*(One).*(Server).*(2).*")).find_previous("a")['href']
        except:
            download_link = None    
        # try:
        #     download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[5]/strong/a/@href')[0]
        # except:
        #     try:
        #         download_link=response_soup.select('div span[class="ws12"] a')[1]['href']
        #     except:
        #         try:
        #             download_link = response_soup.find(string='Download All in One Server 2').find_previous('a')['href']
        #         except:
        #             try:
        #                download_link = response_soup.find(string= "Download All in One (Server 2)").find_previous('a')['href'] 
        #             except:
        #                 try:
        #                     download_link = response_soup.find(string= "All in One – ( Zip File ) Server 2").find_previous('a')['href']   
        #                 except:
        #                     try:
        #                         download_link = response_soup.find(string= "Download All in One Server From 2").find_previous('a')['href'] 
        #                     except:
        #                         try:    
        #                             download_link = response_soup.find(string= "Download All in One zip Server 2").find_previous('a')['href']    
        #                         except:
        #                             download_link=".html"         
        # if download_link.endswith(".htm") or download_link.endswith(".html"):
        #     try:
        #         download_link = dom.xpath('//*[@id="the-post"]/div/div[2]/p[6]/strong/a/@href')[0]
        #     except:
        #         download_link=None
    #REFACTOR RESPONSE ELEMENT CODE BLOCK***THIS IS FOR TESTING PURPOSE ONLY*** LINE 116-124                              
    # response_elements = response_soup.select('li strong a')
    # if response_elements==[]:
    #    response_elements = response_soup.select('p span strong a')
    # if response_elements==[]:
    #     response_elements = response_soup.select('tr td div[class="wpmd"] a')    
    # if response_elements==[]:
    #    response_elements = response_soup.select('span[style="color: #99cc00;"] a')
    # if response_elements==[]:
    #     response_elements = response_soup.select('span[style="color: #ff99cc;"] a')

    response_group = [

        response_soup.select('li strong a'), 
        response_soup.select('p span strong a'),
        response_soup.select('tr td div[class="wpmd"] a'),
        response_soup.select('span[style="color: #99cc00;"] a'),
        response_soup.select('span[style="color: #ff99cc;"] a'),
    
    ]

    valid_group = list(i for i in response_group if i!=[])
    if len(valid_group)>=1:
        response_elements = valid_group[0]
    else:
        return None                
    print("Album Art Link : " ,art_link)
    print("Album Download Link : " ,download_link)   
    songs_collection=[]
    cnt=1
    for element in response_elements:
        try:
            song_link = element['href']
            song_title = element.text
            #REGEX WOULD WORK BETTER HERE
            keywords=['Server','Apple Store','Amazon Store','Youtube','Apple Music','ITunes','Amazon Music','Buy Album',"Download Album"]
            keyword=[i for i in keywords if i in song_title]
            if any(keyword):
                continue
            elif song_title is None:
                continue  
            elif song_title.startswith('Download'):
               song_title=song_title[8:] 
            songs_collection.append((song_title,song_link))
            print("---TRACK "+str(cnt)+"--- "+song_title)
        except:
            pass
        cnt+=1
            #song_title=j.text
            #temp_songs_dict.append((song_title,"@#$%@^!"))
    #print(songs_collection)
    return art_link,download_link,songs_collection,      

for i in range(198,215):
   print('_________________________________Page : '+str(i)+'__________________________________________________')
   url_albums = "https://songslover.vip/category/tracks/page/"+str(i)
   fetch_details(url_albums,track=True)




        #result = [] #use enum/dict object generator
        #soup_elements = soup.select('article h2 a')
        #for element in soup_elements:
            #temp_result = {}
            # try:
            #     artist,title=element.text.split(' –')
            # except: 
            #     title = artist = element.text
            # artist = artist.strip()
            # title = title.strip()     
            # link = element['href']
            # temp_result['artist']=artist 
            # temp_result['title']=title
            # temp_result['link']= link
            # result.append(temp_result)