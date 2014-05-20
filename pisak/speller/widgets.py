'''
Definitions of widgets specific to speller applet
'''
from gi.repository import Mx, GObject
import pisak.widgets
from pisak.res import dims


class Button(Mx.Button):
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


class Key(Mx.Button):
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
    
    def __init__(self):
        self.text = "?"
        self.alt_text = "?"
        super().__init__()
        self.set_size(dims.MENU_BUTTON_H_PX, dims.MENU_BUTTON_H_PX)
    
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
    
    def do_set_property(self, spec, value):
        """
        Introspect object properties and set the value.
        """
        attribute = self.__class__.__dict__.get(spec.name)
        if attribute is not None and isinstance(attribute, property):
            attribute.fset(self, value)
        else:
            super().do_set_property(spec, value)
    
    def do_get_property(self, spec):
        """
        Introspect object properties and get the value.
        """
        attribute = self.__class__.__dict__.get(spec.name)
        if attribute is not None and isinstance(attribute, property):
            return attribute.fget(self)
        else:
            super().do_get_property(self, spec)


class Text(Mx.Label):
    __gtype_name__ = "PisakSpellerText"
    def __init__(self):
        super().__init__()
        self.set_text("Foobar")

class Prediction(Mx.Button):
    __gtype_name__ = "PisakSpellerPrediction"
    __gproperties__ = {
        "dictionary": (
            GObject.TYPE_STRING,
            "prediction dictionary",
            "path to source of prediction words",
            "",
            GObject.PARAM_READWRITE)}

    def __init__(self):
        super().__init__()
        self.set_size(dims.MENU_BUTTON_W_PX, dims.MENU_BUTTON_H_PX)

