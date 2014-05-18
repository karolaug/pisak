'''
Definitions of widgets specific to speller applet
'''
from gi.repository import Mx, GObject
import pisak.widgets


class Button(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerButton"
    __gproperties__ = {
        "speller_function": (
            GObject.TYPE_STRING,
            "speller function",
            "speller function",
            "noop",
            GObject.PARAM_READWRITE)
    }
    def __init__(self):
        super().__init__()
        
        
class Key(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerKey"
    __gproperties__ = {
        "text": (
            GObject.TYPE_STRING,
            "key text",
            "string appended to a text",
            " ",
            GObject.PARAM_READWRITE),
        "alt_text": (
            GObject.TYPE_STRING,
            "alt key text",
            "AltGr string appended to a text",
            "?",
            GObject.PARAM_READWRITE)
    }
    __gsignals__ = {
        "writing": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }
    def __init__(self):
        super().__init__()
        self.connect('activate', spell)
        self.text = self.get_property('text')
        self.alt_text = self.get_property('alt_text')

    def spell(self, event):
        self.emit('writing', self.key) # tu chyba nie trzeba tego key, coś z alt zrobić

class Text(Mx.Notebook):
    __gtype_name__ = "PisakSpellerText"
    
    def __init__(self):
        super().__init__()
        self.text_field = Clutter.Text()
        self.add_child(self.text_field)
        self.connect('writing', write)

    def write(self, event, text): # i tu bez event - dogadac
        self.text_field.insert_text(text, -1) # i tu wtedy jakby Key.key
        
        
class Prediction(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerPrediction"
    __gproperties__ = {
        "dictionary": (
            GObject.TYPE_STRING,
            "prediction dictionary",
            "path to source of prediction words",
            "",
            GObject.PARAM_READWRITE)}
    __gsignals__ = {
        "writing": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }

    def __init__(self):
        super().__init__()
