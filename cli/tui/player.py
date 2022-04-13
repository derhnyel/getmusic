import time
import sys
import curses
import playback
from utils.helpers import debounce
from cli.tui.nowplaying import NowPlaying
from cli.tui.search import Search

from threading import Thread, Lock




# from curses import wrapper
# from curses import textpad
# from curses import panel
#curses.initscr()
# curses.noecho()         # do not echo input
# curses.cbreak()         # do not wait for Enter after input
# curses.curs_set(False)
# stdscr.keypad(True)



starttime = time.time()
lock = Lock()

class Player:
    def __init__(self,stdscr):
        '''Initializes the terminal-based GUI'''
        
        self.stdscr = stdscr
        self.tracklist_uri = None
        self.pause_updates = False

        self.app_name = "GETMUSIC!"
        self.engine = None
        self.status = dict(shuffle_state=False,repeat_state="off",is_playing=False,player_time=None,progress=None,duration=None,item=dict())#"items the dictionary of currently playing track with details like artist name,download etc.")
        
        #Events
        self.events = {
            155: self.handle_exit,
            27: self.handle_exit,
            ord("q"): self.handle_exit,
            9: self.select_next_component,
            curses.KEY_RESIZE: self.handle_resize,
            ord("d"): self.show_device_menu,
            ord("/"): self.show_search_bar,
            ord(" "): self.toggle_playback,
            ord("p"): self.previous_track,
            ord("n"): self.next_track,
            ord("s"): self.toggle_shuffle,
            ord("r"): self.cycle_repeat,
            curses.KEY_RIGHT: self.seek_forward,
            curses.KEY_LEFT: self.seek_backward,
        }

        # window size
        scry, scrx = self.stdscr.getmaxyx()

        # UI components
        self.components = [
            TracksMenu(stdscr,self.engine,self.play_track, self.status),
            LibraryMenu(stdscr,self.engine, self.change_tracklist),
            PlaylistMenu(stdscr,self.engine, self.change_tracklist),
            NowPlaying(stdscr),
        ]
        self.search_component = Search(self.stdscr, self.engine,
                                            self.search)
        self.device_menu_component = DeviceMenu(self.stdscr, self.engine,
                                                self.select_device,
                                                self.hide_popup)

        # Active component
        self.active_component = 0
        self.components[0].activate()

        # Popups
        self.popup = None 

         # Set initial tracklist
         # Check for Previous Session
        if self.status and 'context' in self.status and type(self.status["context"]) is dict and 'uri' in self.status["context"]:
            self.change_tracklist(
                self.api.get_playlist_tracks(self.status["context"]["uri"]), "Previous Session")
        else:
            self.change_tracklist(self.api.get_top_tracks(), "Top Tracks")
    
        # playing every second in a new thread
        playback_loop = Thread(target=self.on_eos)
        playback_loop.daemon = True
        playback_loop.start()

        # Initial render
        self.render()

        status_loop = Thread(target=self.status_loop)
        status_loop.daemon = True
        status_loop.start()

        # Start the main event loop (used for responding to key presses and keeping the main process running)
        while 1:
            try:
                # capture and handle key press
                key = self.stdscr.getch()
                if key in self.events.keys():
                    # run the event handler for the key
                    self.events[key]()
                elif self.popup:
                    # or pass it to the active popup
                    self.popup.receive_input(key)
                else:
                    # or pass the input to the active component
                    self.components[self.active_component].receive_input(
                        key)
                # re-render
                self.render()
            except KeyboardInterrupt:
                sys.exit(0)

    def render(self):
        self.stdscr.erase()
        for component in self.components:
            # render each component
            component.render(self.status)
        if self.popup:
            self.popup.render()
        self.stdscr.refresh()

    def change_tracklist(self, tracks, title, tracklist_uri=None):
        self.components[0].update_tracks(tracks, title)
        self.tracklist_uri = tracklist_uri
        self.activate_tracklist()
    
    def select_next_component(self):
        if self.popup:
            return
        # visually de-activate the current component
        self.components[self.active_component].deactivate()
        # incremement the active component (or go back to start)
        self.active_component = (
            self.active_component +
            1 if self.active_component < len(self.components) - 1 else 0)
        # skip read-only components
        if self.components[self.active_component].interactive:
            self.components[self.active_component].activate()
        else:
            self.select_next_component()
    
    #Set track to a collection of neccesary details
    def play_track(self,track):
        if track['type'] == 'playlist':
            self.change_tracklist(self.api.get_playlist_tracks(
                track['id'] if track['id'] else track['uri']), track['name'], track['uri'])
            return
        if track['type'] == 'show':
            self.change_tracklist(self.api.show_episodes(
                track['id']), track['name'], track['uri'])
            return
        if self.device_id:
            if self.tracklist_uri:
                self.api.start_playback(self.device_id, None,
                                        self.tracklist_uri, {"uri": track["uri"]})
            else:
                self.api.start_playback(
                    self.device_id,
                    list(map(self.__map_tracklist, filter(self.__filter_tracklist,
                                                          self.components[0].tracks))),
                    None,
                    {"uri": track["uri"]},
                )

    def on_eos(self):
        while 1:
            if playback.get_playback_state():
                self.status['duration']= playback.get_duration() 
                if playback.eos() and not self.pause_updates:
                    playback.play_next()       
            time.sleep(1 - ((time.time() - starttime) % 1))    


    def status_loop(self):
        while 1:
            if not self.pause_updates:
                self.status["is_playing"]=playback.get_playback_state()                
                self.status['progress'] = playback.get_time()
                self.components[0].refresh_now_playing(self.status['progress'])

            with lock:
                if not self.pause_updates:
                    self.render()
            time.sleep(1 - ((time.time() - starttime) % 1))        

    @debounce(0.5)
    def previous_track(self):
        playback.play_previous()

    @debounce(0.5)
    def toggle_playback(self):
        self.status['is_playing'] = playback.play_pause()

    @debounce(0.5)
    def next_track(self):
        playback.play_next()

    @debounce(1.5)
    def toggle_shuffle(self):
        self.status['shuffle_state'] = playback.shuffle()

    @debounce(1.5)
    def cycle_repeat(self):
        repeat,cycle = playback.repeat()
        if cycle:
            self.status["repeat_state"] == "context"
        elif repeat:
            self.status["repeat_state"] == "track" 
        else:
            self.status["repeat_state"] == "off"

    @debounce(2)
    def seek_forward(self):
        playback.seek_forward(10)
        self.status["progress"] = playback.get_time().get_timestamp_str()

    @debounce(2)
    def seek_backward(self):
        playback.seek_forward(10,forward=False)
        self.status["progress"] = playback.get_time().get_timestamp_str() 

            
    def search(self, query):
        self.hide_popup()
        query = query.strip()
        if query and len(query) > 1:
            #engine search
            results = self.api.search(query)
            self.change_tracklist(results, "Searching: " + query)
            self.render()

    def activate_tracklist(self):
        self.components[self.active_component].deactivate()
        self.active_component = 0
        self.components[self.active_component].activate()

    @debounce(2)
    def show_device_menu(self):
        self.components[self.active_component].deactivate()
        self.popup = self.device_menu_component
        self.popup.restart()
        self.popup.activate()
        self.render()

    def show_search_bar(self):
        if self.popup:
            return
        self.pause_updates = True
        self.popup = self.search_component
        self.components[self.active_component].deactivate()
        self.popup.activate()
        self.render()

    def select_device(self, device_id):
        self.device_id = device_id

    def hide_popup(self):
        if self.popup:
            self.popup.deactivate()
        self.popup = None
        self.components[self.active_component].activate()
        self.pause_updates = False
        self.stdscr.clear()
        self.render()

    def handle_resize(self):
        for component in self.components:
            # render each component
            component.restart()
        self.stdscr.clear()

    def handle_exit(self):
        if self.popup:
            self.hide_popup()
        else:
            sys.exit(0)

    def __filter_tracklist(self, track):
        return track["type"] == 'track'

    def __map_tracklist(self, track):
        return track["uri"]

                    
    






             
            



    
            



        
        



