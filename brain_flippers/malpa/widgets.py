'''
Widgets dedicated for Malpa game
'''
from gi.repository import Mx, Clutter
import random
import itertools
from gi.overrides import GObject
from pisak.widgets import PropertyAdapter


class MomentaryButton(Mx.Button):
    __gtype_name__ = "BrainMomentaryButton"

    def __init__(self):
        super().__init__()
        self.index = 0
        self.connect("show", MomentaryButton.schedule_cover)

    def schedule_cover(self, *args):
        self.set_label(str(self.index))
        Clutter.threads_add_timeout(1000, self._cover)

    def _cover(self):
        self.set_label("")


class MomentaryButtonGrid(Clutter.Actor):
    __gtype_name__ = "BrainMomentaryButtonGrid"

    POSITION_LIST = itertools.product(list(range(4)), list(range(8)))
    
    def __init__(self):
        super().__init__()
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
    
    def init_buttons(self, count):
        self.count = count
        self.positions = random.sample(self.POSITION_LIST, self.count) 
        for pos in self.positions:
            button = MomentaryButton()
            self.layout.attach(button, pos[0], pos[1], 1, 1)


class StatusBar(Clutter.Actor):
    __gtype_name__ = "BrainMalpaStatusBar"
    
    def __init__(self):
        super().__init__()
        self.score_display = Clutter.Label()
        self.lives_display = Clutter.Label()
        self.add_child(self.score_display)
        self.add_child(self.lives_display)


class Logic(GObject.GObject, PropertyAdapter):
    __gtype_name__ = "BrainMalpaLogic"
    
    __gproperties__ = {
        "board": (MomentaryButtonGrid.__gtype__, "", "", GObject.PARAM_WRITABLE),
        "status": (StatusBar.__gtype__, "", "", GObject.PARAM_WRITABLE)
    }
    