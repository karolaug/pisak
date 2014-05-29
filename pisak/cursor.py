'''
Module handles cursor-style (stream of coordinates) input in JSON layout.
'''
from gi.repository import GObject, Clutter
from time import time

class Group(Clutter.Actor):
    __gtype_name__ = "PisakCursorGroup"
    
    __gproperties__ = {
        "timeout": (
            GObject.TYPE_INT,
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
        self.timeout = 1600
        self.locked = False
        self._init_sprite()
        GObject.idle_add(self.work)

    def _init_sprite(self):
        self.sprite = Clutter.Actor()
        self.sprite.set_size(20, 20)
        self.sprite.set_background_color(Clutter.Color.new(255, 255, 0, 255))

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
        # TODO: read coords from stream
        return (256, 256)
    
    def update_sprite(self, coords):
        self.sprite.set_position(coords[0], coords[1])
    
    def find_actor(self, coords):
        # TODO: search
        return None
    
    def work(self):
        coords = self.read_coords()
        self.update_sprite(coords)
        actor = self.find_actor(coords)
        if actor is not None:
            if actor == self.hover_actor:
                if time.time() - self.hover_start > self._timeout:
                    actor.activate()
            else:
                # reset timeout
                self.hover_start = time.time()
        return True
                    