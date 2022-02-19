
#https://justnaija.com/music/album/page/1-19
#https://justnaija.com/music-mp3/1-286
jt = ssp.select("main article aside a")
jp = ssp.select("main article h3 a")
jimg = ssp.select("main article img")
for index in range(len(jp)):
        title=jp[index].text
        link=jp[index]['href']
        artist=jt[index].text
        art_link=jimg[index]['data-src']

####Tracks
        artist,title=jp[index].text.split("–")
        # try:
        #     title,ft= tit_ft.split("ft.")

        # except:
        #     title = tit_ft    
       


pg = sss.select('div[class="mu-o-c"] div[class="mu-o-unit-c"] div[class="album-side-1"]')
#download_link for both tracks and albums
download_link = sss.select('p[class="song-download"] a')[0]['href']
for i in pg:
    song_link = i.h4.a['href']
    song_title = i.h4.a.text + i.span.text if i.span!=None else i.h4.a.text  
    if i.span!=None:
        #composer = i.strong.text + i.span.text
        song_title = i.h4.a.text + i.span.text

    else:
        #composer = i.strong.text '
        song_title = i.h4.a.text     