'''
Definitions of widgets specific to speller applet
'''
from gi.repository import Mx, GObject, Clutter
import pisak.widgets
from pisak.res import dims


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
        self.set_size(dims.MENU_BUTTON_W_PX, dims.MENU_BUTTON_H_PX)

    @property
    def speller_function(self):
        return self._speller_function

    @speller_function.setter
    def speller_function(self, value):
        self._speller_function = value
        self.assign_function(value)

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
        self.text = "?"
        self.alt_text = "?"
        super().__init__()
        self.set_size(dims.MENU_BUTTON_H_PX, dims.MENU_BUTTON_H_PX)
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
        
    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = str(value)
        self.set_label(self.text)
    
    @property
    def alt_text(self):
        return self._alt_text
    
    @alt_text.setter
    def alt_text(self, value):
        self._alt_text = str(value)


class Text(Mx.Label):
    __gtype_name__ = "PisakSpellerText"
    def __init__(self):
        super().__init__()
        self.set_text("Foobar")

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
        self.set_size(dims.MENU_BUTTON_W_PX, dims.MENU_BUTTON_H_PX)

    def update_button(self):
        raise NotImplementedError()
