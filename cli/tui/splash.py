
import time
import curses


def display(SPLASH_TEXT,root):
   '''Display a splash screen'''
   root.border(0)
   root.refresh()
   
   time.sleep(0.5)

   centreY = (int)(curses.LINES / 2)
   centreX = (int)(curses.COLS / 2)
   halfSplashLen = (int)(len(SPLASH_TEXT) / 2)

   win = curses.newwin(5, len(SPLASH_TEXT) + 6,centreY - 2, centreX - halfSplashLen - 3)
   win.border(0)
   win.refresh()

   complete = False
   counter = 0
   while (not complete):
        time.sleep(0.03)
        root.addstr(centreY, centreX - halfSplashLen,
                    SPLASH_TEXT[:counter], curses.A_BOLD)
        counter += 1
        root.refresh()

        if (counter >= len(SPLASH_TEXT)):
            complete = True

   time.sleep(1)
   curses.beep()
display("                          GETMUSIC                          ",root = curses.initscr())

