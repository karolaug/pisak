'''
Widgets dedicated for Safe game
'''
from gi.repository import Mx, Clutter, GObject
from random import randint
from pisak.widgets import PropertyAdapter

class Numpad(Clutter.Actor):
    __gtype_name__ = "BrainNumpad"
    
    def __init__(self):
        super().__init__()
        self.layout = Clutter.GridLayout()
        self.layout.set_column_homogeneous(True)
        self.layout.set_row_homogeneous(True)
        self.set_layout_manager(self.layout)
        self.all_clicked = []
        self.init_buttons()

    def init_buttons(self):
        self.buttons = (self.set_button(digit+1) for digit in range(9))
        for row in range(3):
            for column in range(3):
                self.layout.attach(next(self.buttons), column, row, 1, 1)

    def set_button(self, digit):
        button = Mx.Button()
        button.set_label(str(digit))
        button.connect("clicked", self.get_clicked)
        return button

    def get_clicked(self, button):
        self.clicked = button.get_label()
        self.all_clicked.append(self.clicked)

class Code(Mx.Label, PropertyAdapter):
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

    def generate_code(self, code_length):
        self.code = [randint(1, 9) for i in range(int(code_length))]

    def convert_text(self):
        self.text = ''.join([str(digit) for digit in self.code])
        self.set_text(self.text)

    def next_lvl(self):
        code_length = len(self.code)
        self.generate_code(code_length + int(self.lvl_diff))
        self.convert_text()
    
