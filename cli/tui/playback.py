import pyglet
import random
from enum import Enum
from cli.download import download_file


SUPPORTED_FORMATS = ['au', 'mp2', 'mp3',
                         'ogg', 'wav', 'wma', 'flac', 'm4a','/']

class Duration(object):
    '''Stores the duration of a track'''
    
    def __init__(self, hours=0, minutes=0, seconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.totalseconds = (hours * 3600) + (minutes * 60) + seconds

    def set_from_sec(self, sec):
        self.hours = int(sec / 3600)
        self.minutes = int(sec / 60) % 60
        self.seconds = int(sec) % 60
        self.totalseconds = sec
    
    #convert to seconds

    def get_timestamp_str(self):
        '''Returns a string-type timestamp in the format of hh:mm:ss'''
        return '{}:{}:{}'.format('{}'.format(self.hours).rjust(2, '0'), '{}'.format(self.minutes).rjust(2, '0'), '{}'.format(self.seconds).rjust(2, '0'))



class Playback():

    def __init__(self):
        self.player = None
        self.download_uri = None
        self.info = None
        self.temp_file = None
        self.duration = None
        self.current_index=0
        self.score =0
        self.playlist = []
        self.shuffle = False
        self.shuffle_list=[]
        self.repeat = False


    def add_to_playlist(self,tracklist,valid=False,playing=False):
        '''Appends the provided files to the playlist, first checking for their existence and then if they are supported'''
        count = 0
        for track in tracklist:
            if track in self.playlist:
                self.playlist.remove(track)    
            if valid or any(list(_format for format_ in SUPPORTED_FORMAT if track.endswith(format_))):
                if playing and len(self.playlist) is not 0:
                    self.playlist.insert(self.current_index+1,track)
                    self.current_index+=1
                else:
                    self.playlist.append(track)
                    count += 1
        return count


    def rem_from_playlist(self,index):
        '''Removes the playlist item at the specified index'''
        for i in range(len(index) - 1, -1, -1):
            index = int(index[i])
            del self.playlist[index - 1]

            if self.current_index == index:
                self.stop()
                self.current_index = 0
            elif self.current_index > index:
                self.current_index -= 1


    def clear_playlist():
        '''Clears all songs from the playlist'''
        self.playlist.clear()

    def Repeat(self):
        if self.player is not None:
           self.player.loop =  False if self.player.loop else True
            
    def stream(self,download_uri,referer=None):
        ##stream/ download audio files
        if download_uri.startswith('https://') and (not download_uri.endswith('zip')):
            self.download_uri = download_uri
            self.temp_file = download_file(download_uri, referer=referer)
            self.add_to_playlist([self.temp_file], valid=True,playing=True)
            self.stop()
            self.start_play(self.temp_file)
          
    def start_play(self,audio_file):
        '''Begins playback of the specified file'''

        if self.player is not None:
            self.stop()
        # Create new player
        self.player = pyglet.media.Player()
        self.player.on_eos = self.on_eos
        self.player.push_handlers(on_eos=self.player.on_eos)
        source = pyglet.media.load(audio_file,streaming=True)
        self.player.queue(source)
        self.player.play()
        self.get_info()
            
    def on_eos(self):
        self.play_next()

    def stop(self):
        if self.player is not None:
            self.player.pause()
            self.player = None

    def play_next(self):
        '''Advances the current track index to the next track in the playlist'''
        if self.shuffle and len(self.playlist) > 1:
            if self.current_index == self.shuffle_list[-1]: 
                self.current_index = random.randint(0,len(self.playlist))
                if self.current_index not in self.shuffle_list:
                    self.shuffle_list.append(self.current_index)
                    self.score += 1
            else:
                self.current_index=self.shuffle_list[self.score]
                self.score += 1
        else:
            if len(self.playlist)-1 > self.current_index:
                if not self.repeat:
                    self.current_index = (self.current_index) + 1 #% len(self.playlist)
            else:
                # playlist.clear if repeat is not on playlist
                # ||||| if repeat on playlist
                self.current_index = 0
        self.play_current()
            
    def play_prev(self):
        '''Returns the current track index to the previous track in the playlist'''
        if self.shuffle and len(self.playlist) > 1:
            if self.current_index == self.shuffle_list[-1]:
                self.current_index = self.shuffle_list[-2]
                if self.score < 1:
                    self.score=0
                else:
                    self.score-=1
            else:
                self.current_index=self.shuffle_list[self.score]
                self.score -= 1
        if len(self.playlist) > 0 and self.current_index > 0:
            if not self.repeat:
                self.current_index = (self.current_index - 1) #% len(self.playlist)
        else:
            self.current_index=0
        self.play_current()    
    
    def play_playlist_no(self,playlist_no):
        '''Plays the song at the specified index in the playlist'''
        self.current_index = playlist_no - 1
        self.play_current()

    def seek(self,timestamp):
        '''Seeks to the provided timestamp'''
        if self.player is not None:
            self.player.source.seek(timestamp)
        self.duration = self.duration-timestamp    

    def play_pause(self):
        '''Toggles between playing and pausing of the current playback'''
        if self.player is not None:
            if self.player.playing:
                self.player.pause()
            else:
                self.player.play()
        else:
            self.play_current()

    def play_current(self):
        if self.current_index < len(self.playlist):
                self.start_play(self.playlist[self.current_index])
        elif self.temp_file is not None:
            self.start_play(self.temp_file)
    
    def get_time(self):
        '''Returns the current playing time of the current track.'''
        duration = Duration()
        if (self.player is not None):
            duration.set_from_sec(self.player.time)
        return duration    
 
    def get_duration(self):
        '''Returns the total playing time of the current track.'''
        duration = Duration()
        if (self.player is not None):
            if self.player.source.duration:
                duration.set_from_sec(self.player.source.duration)
        return duration        
    
    def get_info(self):
        '''Returns a tuple of three objects: trackInfo, audioFormat, and trackDuration.
        Available trackInfo properties (accessible as info.property_name):     title, album, author, year, track, genre, copyright, comment
        Available audioFormat properties (accessible as audiof.property_name): channels, sample_size, sample_rate
        Available trackDuration properties (accessible as trackDuration.property_name): hours, minutes, seconds'''
        info = None
        audiof = None
        if (self.player is not None):
            if self.player.source.info:
                info = self.player.source.info
            if self.player.source.audio_format:
                audiof = self.player.source.audio_format
        duration = self.get_duration().get_timestamp_str()
        self.info = dict(info=info, audio_format=audiof, duration=duration)
        self.duration = sum(x * float(t) for x, t in zip([3600, 60, 1], duration.split(":")))
