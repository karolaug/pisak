'''
Widgets dedicated for Safe game
'''
from gi.repository import Mx, Clutter, GObject
import pisak.widgets
from brain_flippers import widgets
from brain_flippers.malpa.widgets import StatusLabel
import random
import time


class Numpad(Clutter.Actor):
    __gtype_name__ = "BrainNumpad"
    
    __gsignals__ = {    
        "digit": (GObject.SIGNAL_RUN_FIRST, None, [int])
    }
    
    def __init__(self):
        super().__init__()
        self.layout = Clutter.GridLayout()
        self.layout.set_column_homogeneous(True)
        self.layout.set_row_homogeneous(True)
        self.set_layout_manager(self.layout)
        self.init_buttons()

    def init_buttons(self):
        self.buttons = (self.set_button(digit) for digit in range(1, 10))
        
        for row in range(3):
            for column in range(3):
                
                self.layout.attach(next(self.buttons), column, row, 1, 1)

    def set_button(self, digit):
        button = widgets.Button()
        button.set_style_class("MenuButton")
        button.set_label(str(digit))
        button.connect("activate", self.get_clicked)
        return button

    def get_clicked(self, button):
        self.emit("digit", int(button.get_label()))


class Code(StatusLabel, pisak.widgets.PropertyAdapter):
    __gtype_name__ = "BrainSafeCode"
    __gproperties__ = {"base_code_length": (GObject.TYPE_INT64,
                                            "code length",
                                            "code length of first safe", 
                                            1, 9, 3, GObject.PARAM_READWRITE),
                       "lvl_diff": (GObject.TYPE_INT64, 
                                    "lvl diff", 
                                    "difference of code length for levels", 
                                    1, 6, 1, GObject.PARAM_READWRITE),
                       "nr_lvl": (GObject.TYPE_INT64, 
                                  "number of levels",
                                  "number of levels in the game", 
                                  1, 10, 3, GObject.PARAM_READWRITE)}

    def __init__(self):
        super().__init__()

    @property
    def lvl_diff(self):
        return self._lvl_diff

    @lvl_diff.setter
    def lvl_diff(self, value):
        self._lvl_diff = value

    @property
    def nr_lvl(self):
        return self._nr_lvl

    @nr_lvl.setter
    def nr_lvl(self, value):
        self._nr_lvl = value

    @property
    def base_code_length(self):
        return self._base_code_length

    @base_code_length.setter
    def base_code_length(self, value):
        self._base_code_length = value
        self.generate_code(self.base_code_length)
        self.convert_text()

    def clear(self):
        self.set_text("")
    
    def append(self, digit):
        text = self.get_text() + str(digit)
        self.set_text(text)

    def convert_text(self):
        self.text = ''.join([str(digit) for digit in self.code])
        self.set_text(self.text)

    def next_lvl(self):
        code_length = len(self.code)
        self.generate_code(code_length + int(self.lvl_diff))
        self.convert_text()


class Statusbar(Clutter.Actor):
    __gtype_name__ = "BrainDigitSpanStatus"
    
    def __init__(self):
        self._score = 0
        self._lives = 0
        super().__init__()
        self._init_layout()
        self._init_elements()

    def _init_layout(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)

    def _init_elements(self):
        self.score_text = StatusLabel()
        self.add_actor(self.score_text)

        self.lives_text = StatusLabel()
        self.lives_text.set_margin_left(50)
        self.add_actor(self.lives_text)

        self.exit_button = widgets.Button()
        self.exit_button.set_height(100)
        self.exit_button.set_width(250)
        self.exit_button.set_margin_left(300)
        self.exit_button.set_label("Wyjście")
        self.exit_button.set_style_class("MenuButton")
        self.add_actor(self.exit_button)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self._update()

    @property
    def lives(self):
        return self._lives

    @lives.setter
    def lives(self, value):
        self._lives = value
        self._update()

    def _update(self):
        self.score_text.set_text("Punkty: {}".format(self.score))
        self.lives_text.set_text(self.lives * "❤")


class Stimulus(Clutter.Actor):
    __gtype_name__ = "BrainDigitSpanStimulus"

    def __init__(self):
        super().__init__()
        self.stop_time = None
        self._code = None
        self._reversed = None
        self._index = None
        self._init_layout()
        self._init_elements()
        self.set_reactive(True)

    def _init_elements(self):
        self.digit_label = StatusLabel()
        self.add_child(self.digit_label)

    def _init_layout(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

    def show_code(self, code, is_reversed):
        self._reversed = is_reversed
        self._code = list(reversed(code)) if is_reversed else code
        self._index = 0

        self._show_direction()
        self.show()
        Clutter.threads_add_timeout(0, 2000, self._show_digits, None)

    def _show_direction(self):
        if self._reversed:
            label = "Zapamiętaj kod w odwrotnej kolejności"
        else:
            label = "Zapamiętaj kod"
        self.digit_label.set_text(label)
        self.digit_label.show()
        Clutter.threads_add_timeout(0, 1950, self._hide_label, None)

    def _show_digits(self, data):
        self._show_digit()
        Clutter.threads_add_timeout(0, 1200, self._show_next_digit, None)
        return False

    def _show_digit(self):
        digit_text = str(self._code[self._index])
        self.digit_label.set_style_class("digit")
        self.digit_label.set_text(digit_text)
        self.digit_label.show()
        Clutter.threads_add_timeout(0, 1050, self._hide_label, None)

    def _hide_label(self, data):
        self.digit_label.set_style_class("")
        self.digit_label.hide()
        return False

    def _show_next_digit(self, data):
        self._index += 1
        if self._index < len(self._code):
            self._show_digit()
            return True
        else:
            self.hide()
            self.stop_time = time.time()
            return False


class Logic(Clutter.Actor, pisak.widgets.PropertyAdapter):
    __gtype_name__ = "BrainDigitSpanLogic"

    __gproperties__ = {
        "status-bar": (Statusbar.__gtype__, "", "", GObject.PARAM_READWRITE),
        "stimulus": (Stimulus.__gtype__, "", "", GObject.PARAM_READWRITE),
        "code-display": (Code.__gtype__, "", "", GObject.PARAM_READWRITE),
        "keypad": (Numpad.__gtype__, "", "", GObject.PARAM_READWRITE),
        "score-summary": (widgets.Dismissable.__gtype__, "", "", GObject.PARAM_READWRITE),
        "fail-feedback": (widgets.Dismissable.__gtype__, "", "", GObject.PARAM_READWRITE)
    }

    __gsignals__ = {
        "finished": (GObject.SIGNAL_RUN_FIRST, None, [])
    }

    LIVES = 3
    CODE_LIMIT = 13

    def __init__(self):
        super().__init__()
        self.set_fixed_position_set(True)  # bypass layout manager
        self.status_bar = None
        self.code_display = None
        self.stimulus = None
        self.keypad = None
        self.fail_feedback = None
        self.connect("notify::mapped", self._initialize_game)

    def _initialize_game(self, *args):
        self.score = 0
        self.success_count = 0
        self.trials = 0
        self.code_length = 3
        self._start_round()
        self.score_summary.connect("dismissed", self._finish_round)
        self.fail_feedback.connect("dismissed", self._finish_round)

    def _start_round(self):
        self.status_bar.score = self.score

        self.status_bar.lives = self.LIVES - self.trials + self.success_count
        self.reversed = random.choice([i == 0 for i in range(4)])
        self.code = self.generate_code(self.code_length)
        self.entered_code = []
        self.code_display.clear()
        self._key_handle = self.keypad.connect("digit", self._keypad_digit)
        self.stimulus.show_code(self.code, self.reversed)

    def _finish_round(self, *args):
        if self.trials - self.success_count >= self.LIVES:
            self.emit("finished")
        elif self.code_length >= self.CODE_LIMIT:
            self.emit("finished")
        else:
            self._start_round()

    def _keypad_digit(self, keypad, digit):
        # update view
        self.entered_code.append(digit)
        self.code_display.append(digit)
        # check code
        finish_round = False
        if self.code[:len(self.entered_code)] != self.entered_code:
            finish_round = True
        elif len(self.code) <= len(self.entered_code):
            finish_round = True
        # feedback
        if finish_round: 
            self.keypad.disconnect(self._key_handle)
            self.trials += 1
            if self.code == self.entered_code:
                self.feedback_good()
            else:
                self.feedback_bad()

    def feedback_good(self):
        self.code_length += 1
        self.success_count += 1
        solving_time = time.time() - self.stimulus.stop_time
        base_score = self.code_length * 2
        time_bonus = max(int((self.code_length * 2 - solving_time) * 3), 0)
        ratio_bonus = int(max((self.success_count / self.trials) - 0.5, 0) * self.code_length)
        round_score = base_score + time_bonus + ratio_bonus
        self.score += round_score
        entries = [
            ("punkty bazowe", base_score),
            ("bonus za czas", time_bonus),
            ("bonus za skuteczność", ratio_bonus)
        ]
        self.score_summary.display_score(entries, self.score)

    def feedback_bad(self):
        self.fail_feedback.display()

    @staticmethod
    def generate_code(length):
        return [random.choice(range(1, 10)) for _ in range(length)]

    @property
    def status_bar(self):
        return self._status_bar

    @status_bar.setter
    def status_bar(self, value):
        self._status_bar = value

    @property
    def code_display(self):
        return self._code_display

    @code_display.setter
    def code_display(self, value):
        self._code_display = value

    @property
    def stimulus(self):
        return self._stimulus

    @stimulus.setter
    def stimulus(self, value):
        self._stimulus = value

    @property
    def keypad(self):
        return self._keypad

    @keypad.setter
    def keypad(self, value):
        self._keypad = value

    @property
    def score_summary(self):
        return self._score_summary

    @score_summary.setter
    def score_summary(self, value):
        self._score_summary = value

    @property
    def fail_feedback(self):
        return self._fail_feedback

    @fail_feedback.setter
    def fail_feedback(self, value):
        self._fail_feedback = value
