import subprocess
import shutil
import tempfile
import requests
import pyglet
from enum import Enum
from utils import helpers
#from playsound import playsound


class PlaybackState(Enum):
    '''The different states that the player can be in'''
    STOPPED = 1
    PLAYING = 2
    PAUSED = 3

class Playback():

    def __init__(self):
        self.player = None
        self.TEMP_DIR = tempfile.gettempdir()
        self.download_uri = None
        self.playback_state = None
        self.temp_file = None

    def stream(self,download_uri,referer=None):
        ##stream/ download audio files
        self.temp_file = self.download_file(download_uri, referer=referer)
        self.stop()
        self.start_play(self.temp_file)
           
    def start_play(self,audio_file_path):
        '''Begins playback of the specified file'''

        if self.playback_state is not PlaybackState.STOPPED:
            self.stop()

        # Create new player
        self.player = pyglet.media.Player()
        self.player.push_handlers()

        source = pyglet.media.load(audio_file_path)
        self.player.queue(source)
        self.player.play()
        self.playback_state = PlaybackState.PLAYING
    
    def stop(self):
        if self.player is not None:
            self.player.pause()
            self.player=None
        self.playback_state = PlaybackState.STOPPED

    def seek(self,timestamp):
        '''Seeks to the provided timestamp'''
        if self.player is not None:
            self.player.source.seek(timestamp)

    def play_pause(self):
        '''Toggles between playing and pausing of the current playback'''
        if self.playback_state is PlaybackState.PLAYING:
            self.player.pause()
            self.playback_state = PlaybackState.PAUSED
        elif self.playback_state is PlaybackState.PAUSED:
            self.player.play()
            self.playback_state = PlaybackState.PLAYING
        else:
            self.play_current()

    def play_current(self):
        '''Plays the current song'''
        return None


    def download_file(self,uri,referer=None):
        headers = helpers.get_header()
        headers['referer'] = referer if referer is not None else '' 
        temp = tempfile.NamedTemporaryFile(delete=False, dir=self.TEMP_DIR)
        with requests.get(uri,headers=headers,stream=True) as r:
            with open(temp.name, "wb") as f:
                shutil.copyfileobj(r.raw, f)
        return temp.name    
