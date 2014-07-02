'''
Widgets dedicated for Malpa game
'''
from gi.repository import Mx, Clutter
import random
import itertools
from gi.overrides import GObject
from pisak.widgets import PropertyAdapter
import time

class MomentaryButton(Mx.Button):
    __gtype_name__ = "BrainMomentaryButton"

    def __init__(self, number):
        super().__init__()
        self.number = number
        self.connect("show", MomentaryButton.schedule_cover)

    def schedule_cover(self, *args):
        self.set_label(str(self.number))
        Clutter.threads_add_timeout(0, 1000, self._cover)

    def _cover(self):
        self.set_label("*")


class MomentaryButtonGrid(Clutter.Actor):
    __gtype_name__ = "BrainMomentaryButtonGrid"

    POSITION_LIST = list(itertools.product(list(range(4)), list(range(8))))
    
    def __init__(self):
        super().__init__()
        self.layout = Clutter.GridLayout()
        self.layout.set_column_homogeneous(True)
        self.layout.set_row_homogeneous(True)
        self.layout.set_row_spacing(5)
        self.layout.set_column_spacing(5)
        self.set_layout_manager(self.layout)
    
    def init_buttons(self, count):
        self.count = count
        self.buttons = []
        self.positions = random.sample(self.POSITION_LIST, self.count)
        numbers = list(range(1, self.count+1))
        random.shuffle(numbers)
        for pos in self.POSITION_LIST:
            if pos in self.positions:
                number = numbers.pop()
                button = MomentaryButton(number)
            else:
                button = Mx.Button()
                button.set_disabled(True)
            self.buttons.append(button)
            self.layout.attach(button, pos[0], pos[1], 1, 1)

    def clear(self):
        self.remove_all_children()

class StatusBar(Clutter.Actor):
    __gtype_name__ = "BrainMalpaStatusBar"
    
    __gproperties__ = {
        "lives": (GObject.TYPE_INT64, "", "", 0, 100, 3, 
                  GObject.PARAM_READWRITE),
        "score": (GObject.TYPE_INT64, "", "", 0, 1000000, 0, 
                  GObject.PARAM_READWRITE)
    }
    def __init__(self):
        super().__init__()
        self.layout = Clutter.BoxLayout()
        self.layout.set_orientation(Clutter.Orientation(0))
        self.layout.set_spacing(100)
        self.set_layout_manager(self.layout)
        self.lives_display = Mx.Label()
        self.score_display = Mx.Label()
        self.score_display.set_size(100, 50)
        self.lives_display.set_size(100, 50)
        self.add_child(self.score_display)
        self.add_child(self.lives_display)
        
    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
        self.lives_display.set_text(''.join(["Życie: ", value * u"\u2764"]))

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.score_display.set_text(''.join(["Punkty: ", str(value)]))

class Logic(Clutter.Actor, PropertyAdapter):
    __gtype_name__ = "BrainMalpaLogic"

    __gproperties__ = {
        "board": (MomentaryButtonGrid.__gtype__, "", "", 
                  GObject.PARAM_WRITABLE),
        "status-bar": (StatusBar.__gtype__, "", "", GObject.PARAM_READWRITE),
        "game-screen": (Clutter.Actor.__gtype__, "", "", GObject.PARAM_READWRITE),
        "menu-screen": (Clutter.Actor.__gtype__, "", "", GObject.PARAM_READWRITE),
        "end-screen": (Clutter.Actor.__gtype__, "", "", GObject.PARAM_READWRITE),
    }

    __gsignals__ = {
        "finished": (GObject.SIGNAL_RUN_FIRST, None, [])
    }

    def __init__(self):
        super().__init__()
        self.set_fixed_position_set(True)  # bypass layout manager
        self.status_bar = None
        self.board = None
        self.end_screen = None
        self.menu_screen = None
        self.game_screen = None
        self.script = Clutter.Script()
        self.connect("notify::mapped", self._initialize_game)

    def _initialize_game(self, *args):
        self.score = 0
        self.lives = 4
        self.success_count = 0
        self.status_bar.score = self.score
        self.status_bar.lives = self.lives
        self.grid_length = 3
        self._start_round()

    def _start_round(self, reverse=False):
        self.board.remove_all_children()
        self.board.init_buttons(self.grid_length)
        for button in self.board.buttons:
            button.connect("clicked", self.check_value)
        if reverse:
            self.button_values = (value for value in 
                                  range(self.board.count, 0, -1))
        else:
            self.button_values = (value for value in 
                                  range(1, self.board.count+1))
        self.button_to_be_clicked = next(self.button_values)
        self.start_time = time.time()

    def _finish_round(self, *args):
        self.grid_length += 1
        change = 4
        if self.success_count < change:
            self._start_round()
        elif self.success_count == change:
            self.grid_length = 3
            self.board.remove_all_children()
            rule_change_info = Clutter.Text()
            info = "Zmiana zasad gry, teraz należy wybierać przyciski od największego do najmniejszego."
            rule_change_info.set_text(info)
            self.board.add_child(rule_change_info)
            Clutter.threads_add_timeout(0, 1000, self._start_round, True)
        elif self.success_count > change and self.success_count < 2*change:
            self._start_round(reverse=True)
        else:
            self.emit("finished")

    def _load_json(self):
        self.script.load_from_file

    def next_round(self):
        self.success_count += 1
        self.feedback_good()
        self._finish_round()

    def check_value(self, button):
        value_clicked = button.number
        if value_clicked == self.button_to_be_clicked:
            try:
                self.button_to_be_clicked = next(self.button_values)
                button.set_label(str(value_clicked))
            except StopIteration:
                self.next_round()
        else:
            self.status_bar.lives -= 1
            if self.status_bar.lives == 0:
                self.emit("finished")
            else:
                self._start_round()

    def feedback_good(self):
        solving_time = time.time() - self.start_time
        base_score = self.grid_length * 2
        time_bonus = max(int((self.grid_length * 2 - solving_time) * 3), 0)
        ratio_bonus = int(max(self.success_count - 0.5, 0) * self.grid_length)
        round_score = base_score + time_bonus + ratio_bonus
        self.score += round_score
        entries = [
            ("punkty bazowe", base_score),
            ("bonus za czas", time_bonus),
            ("bonus za skuteczność", ratio_bonus)
        ]
        self.status_bar.score = self.score

    @property
    def status_bar(self):
        return self._status_bar

    @status_bar.setter
    def status_bar(self, value):
        self._status_bar = value

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    @property
    def end_screen(self):
        return self._end_screen

    @end_screen.setter
    def end_screen(self, value):
        self._end_screen = value

    @property
    def menu_screen(self):
        return self._menu_screen

    @menu_screen.setter
    def menu_screen(self, value):
        self._menu_screen = value

    @property
    def game_screen(self):
        return self._game_screen

    @game_screen.setter
    def game_screen(self, value):
        self._game_screen = value
