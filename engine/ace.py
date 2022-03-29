from engine.root import BaseEngine
import json

class Ace(BaseEngine):
    
    engine_name = "Ace"
    summary = None #get summary

    def __init__(self):
        super().__init__()
        self.site_uri = "https://backendace.1010diy.com/"
        self.request_method = self.GET
    
    #AN API SO URL NOT ALLOWED
    def search(self, query='',page=None,**kwargs):
        """Search Engine with query parameter"""
        #get response object from formated url with query
        response = self.get_response_object(
            url=self.get_formated_url(
                query=query,
                **kwargs),
                **kwargs,
        )
        response = json.loads(response.text.strip("</iframe"))
        # parse json object and extract link along with other details. 

        # The Ace Api contails 3 different paths the query,details,download
        # search method handles the /query and passes the link extracted to the parse parent object
        
        self.results = list(dict(
            title=item['title'],
            artist = item['title'],
            category ='track',
            track_lenght=item['duration'],
            category_art=item['thumbnail'],
            category_video_palyer= item['player'],
            category_details = self.parse_parent_object(item['url'],title=item['title'])) for  item in response['data']['items'])
        return self.results    


    def parse_parent_object(self,link=None,title=None,**kwargs):
        """
        Parses Engine links to individual items to get thier details 
        such as file extension, quality ,download path
        """

        # The parse parent object method handles the /details extracting the individual details along with a download path
        # The download path is passed to the parse_single object method
        details_url = self.get_formated_url(
            url="https://backendace.1010diy.com/",
            params = {'url':link},
            method = self.GET,
            path=("web","free-mp3-finder","detail"),
        )

        #Get json response object when details url is requested
        response = self.get_response_object(
            url=details_url,
            **kwargs,
        )
        response = json.loads(response.text)['data']['audios'] + json.loads(response.text)['data']['videos']
        
        #Extract details
        return list(dict(
            file_size=item['fileSize'],
            quality=item['formatNote'],
            type='track' if item['ext'] in ['mp3', 'ogg','wav',] else 'video' if item['ext'] in ['mp4'] else None,
            category_download=self.parse_single_object(
                item['url'],
                title,
                item['ext'],
                **kwargs)) 
            for item in response)

    def parse_single_object(self,link=None,title=None,category_type=None,**kwargs):
        """
        Parses the source code to return

        :param : link: link found in <json details>
        :type link: 
        :param : title: title of item
        :type title: `str`
        :param : category_type: extension -> mp3,mp4 
        :type category_type: `str`
        :return: a formated download url 
        :rtype: `str`
        """
        # The parse parent object method handles the /download path. formating a url to download the file
        return link if link.startswith('https://') else "https://stream_ace1.1010diy.com/{url}&ext={ext}&title={title}".format(url=link,ext=category_type,title=title)

    def get_url_path(self,**kwargs):
        """PAth to Page Content"""
        return('web','free-mp3-finder','query')

    def get_query_params(self, query=None, **kwargs):
        return dict(q=query,type='youtube',pageToken='')    





