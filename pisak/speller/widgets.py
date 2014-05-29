'''
Definitions of widgets specific to speller applet
'''
from gi.repository import Mx, GObject
import pisak.widgets
from pisak.res import dims


class Button(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerButton"
    __gproperties__ = {
        "function": (
            GObject.TYPE_STRING,
            "speller function",
            "speller function",
            "noop",
            GObject.PARAM_READWRITE),
        "text": (
            GObject.TYPE_STRING,
            "label default text",
            "text displayed on the button",
            "noop",
            GObject.PARAM_READWRITE),
        "alter": (
            GObject.TYPE_STRING,
            "alternative label text",
            "alternative text displayed on the button",
            "?",
            GObject.PARAM_READWRITE)
    }
    
    def __init__(self):
        self.function = None
        self.text = ""
        self.alter = ""
        super().__init__()
        self.set_size((10./7)*dims.MENU_BUTTON_H_PX, dims.MENU_BUTTON_H_PX)
        self.function = None

    def set_alter_label(self):
        self.set_label(self.alter)

    def set_default_label(self):
        self.set_label(self.text)

    @property
    def function(self):
        return self._function

    @function.setter
    def function(self, value):
        self._function = str(value)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
        self.set_label(self.text)

    @property
    def alter(self):
        return self._alter

    @alter.setter
    def alter(self, value):
        self._alter = str(value)
        

class Text(Mx.Label):
    __gtype_name__ = "PisakSpellerText"
    def __init__(self):
        super().__init__()
        self.clutter_text = self.get_clutter_text()

    def get_text(self):
        return self.clutter_text.get_text()

    def get_text_length(self):
        return len(self.clutter_text.get_text())

    def type_text(self, text):
        pos = self.get_text_length()
        self.clutter_text.insert_text(text, pos)

    def delete_char(self):
        pos = self.get_text_length() - 1
        self.delete_text(pos, pos+1)

    def delete_text(self, start_pos, end_pos):
        self.clutter_text.delete_text(start_pos, end_pos)

    def clear_all(self):
        end_pos = self.get_text_length()
        self.delete_text(0, end_pos)

    def get_string(self):
        text = self.get_text()
        start_pos = text.strip().rfind(' ') + 1
        end_pos = self.get_text_length()
        return text[start_pos : end_pos]

    def replace_string(self, text):
        current_text = self.get_text()
        start_pos = current_text.strip().rfind(' ') + 1
        end_pos = self.get_text_length()
        self.delete_text(start_pos, end_pos)
        self.type_text(text)
        

class Key(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerKey"
    __gproperties__ = {
        "text": (
            GObject.TYPE_STRING,
            "key default text",
            "string appended to a text",
            " ",
            GObject.PARAM_READWRITE),
        "altgr": (
            GObject.TYPE_STRING,
            "altgr text",
            "altgr string appended to a text",
            "?",
            GObject.PARAM_READWRITE),
        "special": (
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

    def __init__(self):
        self.text = ""
        self.altgr = ""
        self.special = ""
        self.target = None
        super().__init__()
        self.set_size(dims.MENU_BUTTON_H_PX, dims.MENU_BUTTON_H_PX)
        self.connect("activate", self.type_text)

    def set_default_label(self):
        self.set_label(self.text)
        
    def set_swap_altgr_label(self):
        label = self.get_label()
        if self.altgr.lower() == label.lower():
            if label.islower():
                self.set_label(self.text.lower())
            else:
                self.set_label(self.text)
        else:     
            if label.isalpha() and self.altgr:
                if self.get_label().islower():
                    self.set_label(self.altgr.swapcase())
                else:
                    self.set_label(self.altgr)

    def set_swap_caps_label(self):
        label = self.get_label()
        self.set_label(label.swapcase())

    def set_special_label(self):
        self.set_label(self.special)

    def type_text(self, source):
        text = self.get_label()
        if self.target:
            self.target.type_text(text)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)
        self.set_label(self.text)

    @property
    def altgr(self):
        return self._altgr

    @altgr.setter
    def altgr(self, value):
        self._altgr = str(value)

    @property
    def special(self):
        return self._special

    @special.setter
    def special(self, value):
        self._special = str(value)

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
            GObject.PARAM_READWRITE),
        "order": (
            GObject.TYPE_INT,
            "order number",
            "position in a line for the new words",
            1,
            9,
            1,
            GObject.PARAM_READWRITE),        
        "target": (
            Text.__gtype__,
            "typing target",
            "id of text box to type text",
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        self.dictionary = None
        self.order = None
        self.target = None
        super().__init__()
        self.set_size(dims.MENU_BUTTON_W_PX, dims.MENU_BUTTON_H_PX)
        self.connect("activate", self.replace_string)

    def follow_target(self):
        if self.target:
            text_field = self.target.clutter_text
            text_field.connect("text-changed", self.update_button)

    def replace_string(self, source):
        if self.target:
            self.target.replace_string(self.get_label())

    def update_button(self, source):
        raise NotImplementedError

    @property
    def dictionary(self):
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value):
        self._dictionary = value

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value
        self.follow_target()

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._order = value
