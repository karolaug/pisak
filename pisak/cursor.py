'''
Module handles cursor-style (stream of coordinates) input in JSON layout.
'''
import threading
import time

from gi.repository import GObject, Clutter, Mx
import sys


class Group(Clutter.Actor):
    __gtype_name__ = "PisakCursorGroup"
    
    __gproperties__ = {
        "timeout": (
            GObject.TYPE_UINT,
            "", "",
            0, GObject.G_MAXUINT, 1600,
            GObject.PARAM_READWRITE),
        "locked": (
            GObject.TYPE_BOOLEAN,
            "", "",
            False,
            GObject.PARAM_READWRITE)
    }
    
    def __init__(self):
        super().__init__()
        self.set_layout_manager(Clutter.BinLayout())
        self.timeout = 800
        self.locked = False
        self._init_sprite()
        self.buttons = None
        self.hover_start = None
        self.hover_actor = None
        self.connect("allocation-changed", self._rescan)
        self.worker = threading.Thread(target=self.work, daemon=True)
        self.worker.start()

    def _init_sprite(self):
        self.sprite = Clutter.Actor()
        self.sprite.set_size(20, 20)
        self.sprite.set_background_color(Clutter.Color.new(255, 255, 0, 255))
        self.sprite.set_depth(10.0)
        self.add_actor(self.sprite)

    @property
    def timeout(self):
        return self._timeout * 1000
    
    @timeout.setter
    def timeout(self, value):
        self._timeout = value / 1000
    
    @property
    def locked(self):
        return self._locked
    
    @locked.setter
    def locked(self, value):
        self._locked = value
    
    def read_coords(self):
        line = sys.stdin.readline()
        try:
            line = line.strip()
            fields = line.split(" ")
            print(fields)
            coords = int(float(fields[0])), int(float(fields[1]))
            return coords
        except:
            coords = 0, 0
            return coords
    
    def update_sprite(self, coords):
        print(coords)
        x, y = (coords[0] - self.sprite.get_width() / 2), (coords[1] - self.sprite.get_height() / 2)
        self.sprite.set_position(x, y)
    
    def _rescan(self, source, *args):
        self.buttons = None

    def scan_buttons(self):
        print("scanning")
        to_scan = self.get_children()
        buttons = []
        while len(to_scan) > 0:
            current = to_scan.pop()
            if isinstance(current, Mx.Button):
                print(current.get_transformed_position())
                buttons.append(current)
            to_scan = to_scan + current.get_children()
        self.buttons = buttons
        print(self.buttons)
    
    def find_actor(self, coords):
        if self.buttons is None:
            self.scan_buttons()
        for button in self.buttons:
            (x, y), (w, h) = button.get_transformed_position(), button.get_size()
            if (x <= coords[0]) and (coords[0] <= x + w) \
                    and (y <= coords[1]) and (coords[1] <= y + h):
                return button
        return None 

    def work(self):
        time.sleep(1)
        while True:
            coords = self.read_coords()
            Clutter.threads_enter()
            self.update_sprite(coords)
            actor = self.find_actor(coords)
            Clutter.threads_leave()
            if actor is not None:
                if actor == self.hover_actor:
                    if time.time() - self.hover_start > self._timeout:
                        Clutter.threads_enter()
                        actor.emit("clicked")
                        Clutter.threads_leave()
                        self.hover_start = time.time() + 1.0 # dead time
                else:
                    # reset timeout
                    Clutter.threads_enter()
                    if self.hover_actor is not None:
                        self.hover_actor.set_style_pseudo_class("")
                    self.hover_actor = actor
                    self.hover_actor.set_style_pseudo_class("hover")
                    Clutter.threads_leave()
                    self.hover_start = time.time() 
            else:
                if self.hover_actor is not None:
                    Clutter.threads_enter()
                    self.hover_actor.set_style_pseudo_class("")
                    Clutter.threads_leave()
                    self.hover_actor = None