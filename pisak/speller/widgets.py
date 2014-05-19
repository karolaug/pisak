'''
Definitions of widgets specific to speller applet
'''
from gi.repository import Mx, GObject, Clutter
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
        self.connect("notify::speller-function", lambda *_: self.assign_function())

    def assign_function(self):
        raise NotImplementedError()

    def update_button(self):
        raise NotImplementedError()

        
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
            GObject.PARAM_READWRITE),
        "cl_text": (
            GObject.TYPE_STRING,
            "caps lock key text",
            "CapsLockGr string appended to a text",
            "?",
            GObject.PARAM_READWRITE),
        "special_text": (
            GObject.TYPE_STRING,
            "special key text",
            "SpecialGr string appended to a text",
            "?",
            GObject.PARAM_READWRITE)
    }
    
    __gsignals__ = {
        "writing": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }
    
    def __init__(self):
        super().__init__()
        #self.connect('activate', self.spell)
        self.connect("notify::text", lambda *_: self._init_label())
    
    def _init_label(self):
        self.set_initial_label()
        
    def set_label_text(self, text):
        self.set_label(text)

    def set_initial_label(self):
        text = self.get_property("text")
        self.set_label_text(text)

    def set_alt_label(self):
        alt_text = self.get_property("alt_text")
        self.set_label_text(alt_text)

    def set_cl_label(self):
        cl_text = self.get_property("cl_text")
        self.set_label_text(cl_text)

    def set_special_label(self):
        special_text = self.get_property("special_text")
        self.set_label_text(special_text)

    def update_button(self):
        raise NotImplementedError()

    def spell(self, key, event):
        self.emit('writing', key) # tu chyba nie trzeba tego key, coś z alt zrobić
        

class Text(Mx.BoxLayout):
    __gtype_name__ = "PisakSpellerText"
    
    def __init__(self):
        super().__init__()
        #self.text_field = Clutter.Text()
        #self.add_child(self.text_field)
        #self.connect('writing', self.write)

    def write(self, event, key): # i tu bez event - dogadac
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

    def update_button(self):
        raise NotImplementedError()
