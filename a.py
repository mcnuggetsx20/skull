from Xlib import X, display, Xutil
from ewmh import EWMH
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
ewmh = EWMH()

class Window(object):
    def __init__(self,display):
        win =ewmh.getActiveWindow() 
        ewmh.setWmState(win, 1, '_NET_WM_STATE_ABOVE')

        self.dp = display
        self.screen = self.dp.screen()

        bgsize = 20

        bgpm = self.screen.root.create_pixmap(
                bgsize,
                bgsize,
                self.screen.root_depth,
        )
        
        bggc = self.screen.root.create_gc(
                foreground = self.screen.black_pixel,
                background = self.screen.black_pixel,
        )

        bgpm.fill_rectangle(bggc, 0, 0, bgsize, bgsize)
        bggc.change(foreground=self.screen.white_pixel)

        self.window = self.screen.root.create_window(
                100, 100, 400, 300, 0, 
                self.screen.root_depth,
                X.InputOutput,
                X.CopyFromParent,
                background_pixmap = bgpm,
                colormap = X.CopyFromParent,
        )

        self.WM_DELETE_WINDOW = self.dp.intern_atom('WM_DELETE_WINDOW')
        self.WM_PROTOCOLS = self.dp.intern_atom('WM_PROTOCOLS')

        self.window.set_wm_name('niezle elo')
        self.window.set_wm_icon_name('elo')
        self.window.set_wm_class('niezle', 'elo')
        self.window.set_wm_protocols([self.WM_DELETE_WINDOW])


        self.window.map()

    def loop(self):
        while 1:
            event = self.dp.next_event()
            if event.type == X.DestroyNotify: sys.exit(0)

            elif event.type == X.ClientMessage:
                if event.client_type == self.WM_PROTOCOLS:
                    fmt, data = event.data
                    if fmt == 32 and data[0] == self.WM_DELETE_WINDOW:
                        sys.exit(0)

Window(display.Display()).loop()



