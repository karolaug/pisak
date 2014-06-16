'''
Widgets dedicated for Safe game
'''
from gi.repository import Mx, Clutter
from random import randint

class Numpad(Mx.Grid):
    __gtype_name__ = "BrainNumpad"
    
    def __init__(self):
        super().__init__()


class DigitButton(Mx.Button):
    __gtype_name__ = "BrainDigitButton"

    def __init__(self):
        super().__init__()


class Code(Mx.Label):
    __gtype_name__ = "BrainSafeCode"

    def __init__(self, code_length):
        super().__init__()
        self.generate_code(code_length)
        self.convert_text()
        self.set_text(self.text)

    def generate_code(self, code_length):
        self.code = [randint(1, 9) for i in range(int(code_length))]
        
    def convert_text():
        self.text = ''.join(self.code)

    def next_lvl(diff):
        code_length = len(self.code)
        self.generate_code(code_length + int(diff))
        self.convert_text()
    
