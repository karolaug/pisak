'''
Widgets dedicated for Malpa game
'''
from gi.repository import Mx, Clutter


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

    def __init__(self):
        super().__init__()
    