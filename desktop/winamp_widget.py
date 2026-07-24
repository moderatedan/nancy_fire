#!/usr/bin/env python3
"""
Nancy Fire Amp — Desktop Widget
Loads the exact Winamp skin from localhost:5000/winamp.html
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, WebKit2, Gdk
import os

class WinampWidget(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Nancy Fire Amp")
        self.set_default_size(700, 480)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Widget mode — frameless, always on top
        self.set_decorated(False)
        self.set_keep_above(True)
        
        # Drag support
        self.dragging = False
        self.drag_x = 0
        self.drag_y = 0
        
        # WebKit view
        self.webview = WebKit2.WebView()
        self.webview.set_zoom_level(1.0)
        
        # Load the Winamp skin from localhost
        self.webview.load_uri("http://localhost:5000/winamp.html")
        
        self.add(self.webview)
        self.connect("destroy", Gtk.main_quit)
        
        # Drag events
        self.webview.connect("button-press-event", self.on_mouse_down)
        self.webview.connect("button-release-event", self.on_mouse_up)
        self.webview.connect("motion-notify-event", self.on_mouse_move)
        self.webview.set_events(Gdk.EventMask.BUTTON_PRESS_MASK |
                                Gdk.EventMask.BUTTON_RELEASE_MASK |
                                Gdk.EventMask.POINTER_MOTION_MASK)
        
        self.show_all()
    
    def on_mouse_down(self, widget, event):
        if event.button == 1:
            self.dragging = True
            self.drag_x = event.x_root
            self.drag_y = event.y_root
        return False
    
    def on_mouse_up(self, widget, event):
        if event.button == 1:
            self.dragging = False
        return False
    
    def on_mouse_move(self, widget, event):
        if self.dragging:
            x, y = self.get_position()
            dx = event.x_root - self.drag_x
            dy = event.y_root - self.drag_y
            self.move(x + dx, y + dy)
            self.drag_x = event.x_root
            self.drag_y = event.y_root
        return False

def main():
    win = WinampWidget()
    Gtk.main()

if __name__ == "__main__":
    main()
