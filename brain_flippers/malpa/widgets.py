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

    def __init__(self, number):
        super().__init__()
        self.number = number
        self.connect("show", MomentaryButton.schedule_cover)

    def schedule_cover(self, *args):
        self.set_label(str(self.number))
        Clutter.threads_add_timeout(1000, self._cover)

    def _cover(self):
        self.set_label("")


class MomentaryButtonGrid(Clutter.Actor):
    __gtype_name__ = "BrainMomentaryButtonGrid"

    POSITION_LIST = list(itertools.product(list(range(4)), list(range(8))))
    
    def __init__(self):
        super().__init__()
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
    
    def init_buttons(self, count):
        self.count = count
        self.positions = random.sample(self.POSITION_LIST, self.count) 
        for pos, number in zip(self.positions, range(self.count)):
            button = MomentaryButton(number)
            self.layout.attach(button, pos[0], pos[1], 1, 1)


class StatusBar(Clutter.Actor):
    __gtype_name__ = "BrainMalpaStatusBar"
    
    __gproperties__ = {
        "lives": (GObject.TYPE_INT64, "", "", 3, 0, 100, 
                  GObject.PARAM_READWRITE),
        "score": (GObject.TYPE_INT64, "", "", 0, 0, 1000000, 
                  GObject.PARAM_READWRITE)
    }
    def __init__(self):
        super().__init__()
        self.score_display = Mx.Label()
        self.lives_display = Mx.Label()
        self.add_child(self.score_display)
        self.add_child(self.lives_display)
        
    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
        self.lives_display.set_text(str(value))

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.score_display.set_text(str(value))


class Logic(GObject.GObject, PropertyAdapter):
    __gtype_name__ = "BrainMalpaLogic"
    
    __gproperties__ = {
        "board": (MomentaryButtonGrid.__gtype__, "", "", GObject.PARAM_WRITABLE),
        "status": (StatusBar.__gtype__, "", "", GObject.PARAM_WRITABLE)
    }

    def __init__(self):
        super().__init__()
        self.score = 0
        self.lives = 3

    def good_answer(self):
        self.score += 1000
        self.status.set_score(self.score)
        if self.answers >= self.all_tiles:
            self.puzzle_solved()

    def bad_answer(self):
        if self.lives == 0:
            self.game_over()
        else:
            self.lives -= 1
            self.status.set_lives(self.lives)

    def game_over(self):
        print("Zbyt wiele prób")

    def puzzle_solved(self):
        print("Ułożone")

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.status.set_score(self.score)
        self.status.set_lives(self.lives)