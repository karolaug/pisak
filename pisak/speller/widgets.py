'''
Definitions of widgets specific to speller applet
'''
from gi.repository import Mx, GObject
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


class Text(Mx.Entry):
    __gtype_name__ = "PisakSpellerText"
    def __init__(self):
        super().__init__()
        #self.set_text("Foobar")

    def write(self, event, key): # i tu bez event - dogadac
        self.text_field.insert_text(text, -1) # i tu wtedy jakby Key.key


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
            "altgr text",
            "altgr string appended to a text",
            "?",
            GObject.PARAM_READWRITE),
        "cl_text": (
            GObject.TYPE_STRING,
            "caps text",
            "caps string appended to a text",
            "?",
            GObject.PARAM_READWRITE),
        "special_text": (
            GObject.TYPE_STRING,
            "special text",
            "special string appended to a text",
            "?",
            GObject.PARAM_READWRITE),
        "target": (
            Text.__gtype__,
            "typing target",
            "id of text box to type text",
            GObject.PARAM_READWRITE)
    }

    __gsignals__ = {
        "writing": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }

    def __init__(self):
        self.text = "?"
        self.alt_text = "?"
        self.target = None
        super().__init__()
        self.set_size(dims.MENU_BUTTON_H_PX, dims.MENU_BUTTON_H_PX)
        self.connect("activate", self.type_text)

    def set_alt_label(self):
        self.set_label_text(self.alt_gr_text)

    def set_cl_label(self):
        self.set_label_text(self.caps_text)

    def set_special_label(self):
        special_text = self.get_property("special_text")
        self.set_label_text(special_text)

    def type_text(self, source):
        if self.target:
            text = self.target.get_text() + self.text
            self.target.set_text(text)

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

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value


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
