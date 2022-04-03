import pyglet
from enum import Enum
from cli.download import download_file


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

    def stream(self,download_uri,referer=None):
        ##stream/ download audio files
        self.download_uri = download_uri
        self.temp_file = download_file(download_uri, referer=referer)
        self.stop()
        if not download_uri.endswith('.zip'):
            self.start_play(self.temp_file)
        else:
            return "Zip downloading....."    
           
    def start_play(self,audio_file_path):
        '''Begins playback of the specified file'''

        if self.player is not None:
            self.stop()

        # Create new player
        self.player = pyglet.media.Player()
        self.player.push_handlers()

        source = pyglet.media.load(audio_file_path)
        self.player.queue(source)
        self.player.play()

        self.get_info()
    
    def stop(self):
        if self.player is not None:
            self.player.pause()
            self.player=None


    def seek(self,timestamp):
        '''Seeks to the provided timestamp'''
        if self.player is not None:
            self.player.source.seek(timestamp)
        self.duration = self.duration-timestamp    

    def play_pause(self):
        '''Toggles between playing and pausing of the current playback'''
        if self.player is not None:
            if self.player.time > self.duration and self.duration is not None:
                self.play_current()
            elif self.player.playing:
                self.player.pause()
            else:
                self.player.play()
        else:
            self.play_current()

    def play_current(self):
        if self.temp_file is not None:
            self.start_play(self.temp_file)
        '''Plays the current song'''
    
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
