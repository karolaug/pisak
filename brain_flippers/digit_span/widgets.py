'''
Widgets dedicated for Safe game
'''
from gi.repository import Mx, Clutter, GObject
from random import randint
from pisak import widgets
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
        self.all_clicked = []
        self.init_buttons()

    def init_buttons(self):
        self.buttons = (self.set_button(digit) for digit in range(1, 10))
        
        for row in range(3):
            for column in range(3):
                
                self.layout.attach(next(self.buttons), column, row, 1, 1)

    def set_button(self, digit):
        button = Mx.Button()
        button.set_label(str(digit))
        button.connect("clicked", self.get_clicked)
        return button

    def get_clicked(self, button):
        self.emit("digit", int(button.get_label()))


class Code(Mx.Label, widgets.PropertyAdapter):
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
        super().__init__()
        self._init_layout()
        self._init_elements()

    def _init_layout(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)

    def _init_elements(self):
        self.score_text = Mx.Label()
        self.add_actor(self.score_text)

        self.exit_button = Mx.Button()
        self.exit_button.set_label("Wyjście")
        self.add_actor(self.exit_button)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        self._score = value
        self.score_text.set_text("SCORE: {}".format(self.score))


class Stimulus(Clutter.Actor):
    __gtype_name__ = "BrainDigitSpanStimulus"
    
    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_elements()
        
    def _init_elements(self):
        self.digit_label = Mx.Label()
        self.add_child(self.digit_label)
    
    def _init_layout(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
    
    def show_code(self, code):
        self.show()
        self._code = code
        self._index = 0
        self._show_digit()
        Clutter.threads_add_timeout(0, 1000, self._show_next_digit, None)
    
    def _show_digit(self):
        digit_text = str(self._code[self._index])
        print("DIGIT")
        self.digit_label.set_text(digit_text)
    
    def _show_next_digit(self, data):
        self._index += 1
        if self._index < len(self._code):
            self._show_digit()
            return True
        else:
            self.hide()
            return False


class Logic(Clutter.Actor, widgets.PropertyAdapter):
    __gtype_name__ = "BrainDigitSpanLogic"
    
    __gproperties__ = {
        "status-bar": (Statusbar.__gtype__, "", "", GObject.PARAM_READWRITE),
        "stimulus": (Stimulus.__gtype__, "", "", GObject.PARAM_READWRITE),
        "code-display": (Code.__gtype__, "", "", GObject.PARAM_READWRITE),
        "keypad": (Numpad.__gtype__, "", "", GObject.PARAM_READWRITE)
    }
    
    def __init__(self):
        super().__init__()
        self.set_fixed_position_set(True)  # bypass layout manager
        self.status_bar = None
        self.code_display = None
        self.stimulus = None
        self.keypad = None
        self.connect("notify::mapped", self._initialize_game)
        #self._ready_id = self.connect("parent-set", self._get_ready)
    
    def _get_ready(self, source, old_parent):
        source.disconnect(self._ready_id)
        if self.get_stage():
            self.get_stage().connect("show", self._initialize_game)
        else:
            self._ready_id = source.get_parent().connect("parent-set", self._get_ready)
    
    def _initialize_game(self, *args):
        self.score = 0
        self.code = self.generate_code(4)
        self.entered_code = []
        self.status_bar.score = self.score
        self.code_display.clear()
        self._key_handle = self.keypad.connect("digit", self._keypad_digit)
        self.stimulus.show_code(self.code)
    
    def _keypad_digit(self, keypad, digit):
        self.entered_code.append(digit)
        self.code_display.append(digit)
        if len(self.code) <= len(self.entered_code):
            self.keypad.disconnect(self._key_handle)
            if self.code == self.entered_code:
                self.feedback_good()
            else:
                self.feedback_bad()
            self._initialize_game()
    
    def feedback_good(self):
        print("dobrze")
    
    def feedback_bad(self):
        print("źle")
                
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
