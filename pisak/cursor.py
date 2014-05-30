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
        self.timeout = 1600
        self.locked = False
        self._init_sprite()
        self.buttons = None
        self.hover_start = None
        self.hover_actor = None
        self.worker = threading.Thread(target=self.work, daemon=True)
        self.worker.start()

    def _init_sprite(self):
        self.sprite = Clutter.Actor()
        self.sprite.set_size(20, 20)
        self.sprite.set_background_color(Clutter.Color.new(255, 255, 0, 255))
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
            fields = line.split(" ")
            coords = int(fields[0]), int(fields[1])
            return coords
        except:
            raise Exception("Protocol error")
    
    def update_sprite(self, coords):
        self.sprite.set_position(coords[0], coords[1])
    
    def _scan_buttons(self):
        to_scan = self.get_children()
        buttons = []
        while len(to_scan) > 0:
            current = to_scan.pop()
            if isinstance(current, Mx.Button):
                buttons.append(current)
            to_scan = to_scan + current.get_children()
        self.buttons = buttons
    
    def find_actor(self, coords):
        if self.buttons == None:
            self._scan_buttons()
        for button in self.buttons:
            (x, y), (w, h) = button.get_position(), button.get_size()
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
            Clutter.threads_leave()
            actor = self.find_actor(coords)
            if actor is not None:
                if actor == self.hover_actor:
                    if time.time() - self.hover_start > self._timeout:
                        actor.emit("clicked")
                        self.hover_start = time.time() + 1.0 # dead time
                else:
                    # reset timeout
                    self.hover_actor = actor
                    self.hover_start = time.time() 
