import pyglet
import random
from cli.download import DownloadFile

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

    def get_timestamp_str(self):
        '''Returns a string-type timestamp in the format of hh:mm:ss'''
        return '{}:{}:{}'.format('{}'.format(self.hours).rjust(2, '0'), '{}'.format(self.minutes).rjust(2, '0'), '{}'.format(self.seconds).rjust(2, '0'))

duration = None
info = None
__player__ = None
__download_uri__ = None
__tempfile__ = None
__current_index__ = 0
__playlist__ = list()
__shuffle_list__ = list()
__shuffle_state__ = False
__repeat_state__ = False
__cycle_repeat__= False
__SUPPORTED_FORMATS__ = ['au', 'mp2', 'mp3',
                         'ogg', 'wav', 'wma', 'flac', 'm4a','/']

#_________________________________________Control Playlist_______________________________ 


def add_to_playlist(tracklist,valid=False,playing=False,):
    '''Appends the provided files to the __playlist__, first checking for their existence and then if they are supported'''
    global __playlist__,__current_index__,__shuffle_state__,__shuffle_list__
    count = 0
    for track in tracklist:
        if track in __playlist__:

            __playlist__.remove(track)
            __current_index__= __current_index__-1 if __current_index__>0 else 0    
        if valid or any(list(format_ for format_ in __SUPPORTED_FORMATS__ if track.endswith(format_))):
            if track.startswith('https://'):
                #extract referer if any
                track = DownloadFile(__download_uri__)#, referer=referer)
            if playing and len(__playlist__) is not 0:
                __playlist__.insert(__current_index__+1,track)
                __current_index__+=1
            else:
                __playlist__.append(track)
                count += 1
            if __shuffle_state__:
                __shuffle_list__.append(track) 
    return count


def remove_from_playlist(index):
    global __playlist__,__current_index__
    '''Removes the __playlist__ item at the specified index'''
    for i in range(len(index) - 1, -1, -1):
        index = int(index[i])
        del __playlist__[index - 1]
        if __current_index__ == index:
            stop()
            __current_index__ = 0
        elif __current_index__ > index:
            __current_index__ -= 1

def clear_playlist():
    global __playlist__
    '''Clears all songs from the __playlist__'''
    __playlist__.clear()

#_________________________________________Control Player Actions____________________________________ 


def repeat():
    global __repeat_state__,__cycle_repeat__

    if __cycle_repeat__:
        __repeat_state__ =__cycle_repeat__= False
    elif __repeat_state__:
        __cycle_repeat__ = True
        __repeat_state__ = False
    else:
        __repeat_state__ = True    
    #__repeat_state__ = False if __repeat_state__ else True
    return __repeat_state__,__cycle_repeat__


def shuffle():
    global __shuffle_list__,__shuffle_state__,__current_index__
    if not __shuffle_state__:
        temp_list = __playlist__.copy()
        random.shuffle(temp_list)
        __shuffle_list__ = temp_list
        __current_index__=__shuffle_list__.index(get_current_track()) 
        __shuffle_state__=True
    else:
        
        __current_index__ = __playlist__.index(get_current_track_shuffle())
        __shuffle_state__= False
    return __shuffle_state__     


def seek(timestamp):
    global __player__
    '''Seeks to the provided timestamp'''
    if __player__ is not None:
        __player__.seek(timestamp)

def seek_forward(timestamp,forward=True):
    if __player__ is not None:
        if not eos():
            seek(0.0)
        seek(get_time_now()+timestamp) if forward else seek(get_time_now()-timestamp)
      

def eos(offset=None):
    if __player__ is not None:
        if offset is not None:
            return True if duration+offset < get_time_now() else False
        return __player__._audio_player.buffer_end_submitted
    else:
        False    
        
def volume(level):
    global __player__
    level = level/100  
    __player__.volume(level) 

def stream(__download_uri__,referer=None):
    global download_url,__tempfile__
    ##stream/ download audio files
    if __download_uri__.startswith('https://') and (not __download_uri__.endswith('zip')):
        download_url = __download_uri__
        __tempfile__ = DownloadFile(__download_uri__, referer=referer)
        add_to_playlist([__tempfile__], valid=True,playing=True)
        stop()
        start(__tempfile__)


#_____________________________Control Audio Files Playback________________________________________


def start(audio_file):
    '''Begins playback of the specified file'''
    global __player__
    if __player__ is not None:
        stop()
    # Create new __player__
    __player__ = pyglet.media.Player()
    #__player__.on_eos = play_next
    __player__.push_handlers(on_eos=play_next)
    source = pyglet.media.load(audio_file,streaming=True)
    __player__.queue(source)
    __player__.play()
    get_info()
    #__player__.dispatch_event("on_eos")


def stop():
    global __player__
    if __player__ is not None:
        __player__.pause()
        __player__ = None

def play():
    global __shuffle_list__,__current_index__,__playlist__
    if __current_index__ < len(__playlist__):
            if __shuffle_state__:
                start(__shuffle_list__[__current_index__]) 
            else: start(__playlist__[__current_index__])
    elif __tempfile__ is not None:
        start(__tempfile__)



def play_pause():
    global __player__
    '''Toggles between playing and pausing of the current playback'''
    if __player__ is not None and not eos():
        if __player__.playing:
            __player__.pause()
        else:
            __player__.play()

    elif __current_index__<len(__playlist__):
        play_next()
    else:
        play()    
    return __player__.playing    

    
def play_next():
    global __playlist__,__current_index__
    '''Advances the current track index to the next track in the __playlist__'''
    if len(__playlist__)-1 > __current_index__:
        if not __repeat_state__:
            __current_index__ = (__current_index__) + 1 #% len(__playlist__)
    else:

        if (__cycle_repeat__):
            __current_index__= 0
        elif(__repeat_state__):
            pass        
        else:
            return
    play()       



def play_previous():
    global __playlist__,__current_index__
    '''Returns the current track index to the previous track in the __playlist__'''
    if len(__playlist__) > 0 and __current_index__ > 0:
        if not __repeat_state__:
            __current_index__ = (__current_index__ - 1) #% len(__playlist__)
    else:
        __current_index__= 0
    play()    


def play_playlist_no(playlist_no):
    global __current_index__
    '''Plays the song at the specified index in the __playlist__'''
    __current_index__ = playlist_no - 1
    play()

# _________________Get Attributes of Playback and Player_______________________________


def get_time_now():
    return __player__.time



def get_playback_state():
    return __player__.playing if __player__ is not None else False 



def get_shuffle_state():
    return __shuffle_state__



def get_repeat_state():
    return __repeat_state__


def get_cycle_repeat():
    return __cycle_repeat__   



def get_playlist():
    return __playlist__


def get_shufflelist():
    return __shuffle_list__    


def get_current_track():
    return __playlist__[__current_index__] if __current_index__ < len(__playlist__) else None 

def get_current_track_shuffle():
    return __shuffle_list__[__current_index__] if __current_index__ < len(__shuffle_list__) else None 


def get_current_index():
    return __current_index__


def get_time():
    global __player__
    '''Returns the current playing time of the current track.'''
    duration = Duration()
    if (__player__ is not None):
        duration.set_from_sec(__player__.time)
    return duration    


def get_duration():
    global __player__
    '''Returns the total playing time of the current track.'''
    duration = Duration()
    if (__player__ is not None):
        if __player__.source.duration:
            duration.set_from_sec(__player__.source.duration)   
    return duration


def get_info():
    global __player__,info,duration
    info = None
    audiof = None
    if (__player__ is not None):
        if __player__.source.info:
            info = __player__.source.info
        if __player__.source.audio_format:
            audiof = __player__.source.audio_format
    duration_ = get_duration().get_timestamp_str()
    info = dict(info=info, audio_format=audiof, duration=duration_)
    duration = sum(x * float(t) for x, t in zip([3600, 60, 1], duration_.split(":")))

#pyglet.app.run()