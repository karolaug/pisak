'''
Definitions of widgets specific to speller applet
'''
import threading

from gi.repository import Mx, GObject, Pango

from pisak.speller.prediction import predictor
from pisak import unit
import pisak.widgets


class Button(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerButton"

        
class Text(Mx.Label, pisak.widgets.PropertyAdapter):
    __gtype_name__ = "PisakSpellerText"
    __gproperties__ = {
        "ratio_width": (GObject.TYPE_FLOAT, None, None, 0, 1., 0, GObject.PARAM_READWRITE),
        "ratio_height": (GObject.TYPE_FLOAT, None, None, 0, 1., 0, GObject.PARAM_READWRITE)
    }
    
    def __init__(self):
        super().__init__()
        self.clutter_text = self.get_clutter_text()
        self._set_text_params()

    def _set_text_params(self):
        self.clutter_text.set_line_wrap(True)
        self.clutter_text.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
        
    def get_text(self):
        """
        Return the entire text from the text buffer
        """
        return self.clutter_text.get_text()

    def get_text_length(self):
        """
        Return the number of characters in the text buffer
        """
        return len(self.clutter_text.get_text())

    def type_text(self, text):
        """
        Append the given text to the text buffer
        @param text string passed after a user's actions
        """
        self.clutter_text.insert_text(text, -1)

    def type_unicode_char(self, char):
        """
        Append the given unicode character to the text buffer
        @param char unicode character in the form of unicode escape sequence
        """    
        self.clutter_text.insert_unichar(char)

    def delete_char(self):
        """
        Delete the endmost single character
        """
        pos = self.get_text_length() - 1
        self.clutter_text.delete_text(pos, pos+1)

    def delete_text(self, start_pos, end_pos):
        """
        Delete all characters from positions from the given range
        @param start_pos start position given in characters
        @param end_pos end position given in characters
        """
        self.clutter_text.delete_text(start_pos, end_pos)

    def clear_all(self):
        """
        Clear the entire text buffer
        """
        self.clutter_text.set_text(None)


    def get_endmost_triplet(self):
        """
        Look for and return the first three-word string of characters with no commas
        starting from the end of the text buffer
        """

        text = self.get_text()
        start_pos = None
        last_sentence_list = text.rstrip().split('.')[-1].split()	
        if len(last_sentence_list) >= 1:         
            start_pos = -len(last_sentence_list[-1]) #negative start pos, counted from the end of the sting
        if len(last_sentence_list) >= 2:
            start_pos -= len(last_sentence_list[-2]) + 1
        if len(last_sentence_list) >= 3:
            start_pos -= len(last_sentence_list[-3]) + 2
        if start_pos is not None:        
            return text.rstrip()[start_pos:]
        else:
            return ' '

    def get_endmost_string(self):
        """
        Look for and return the first string of characters with no whitespaces
        starting from the end of the text buffer
        """
        text = self.get_text()
        start_pos = text.rstrip().rfind(' ') + 1
        end_pos = len(text.rstrip())
        return text[start_pos : end_pos]



    def replace_endmost_string(self, text):
        """
        Look for the first string of characters with no whitespaces starting
        from the end of the text buffer and replace it with the given text
        @param text string passed after a user's action
        """
        current_text = self.get_text()
        start_pos = current_text.rstrip().rfind(' ') + 1
        end_pos = self.get_text_length()
        self.delete_text(start_pos, end_pos)
        self.type_text(text)

    def move_cursor_forward(self):
        """
        Move cursor one position forward
        """
        current_position = self.clutter_text.get_cursor_position()
        if current_position < self.get_text_length():
            self.clutter_text.set_cursor_position(current_position+1)

    def move_cursor_backward(self):
        """
        Move cursor one position backward
        """
        current_position = self.clutter_text.get_cursor_position()
        if current_position > 0:
            self.clutter_text.set_cursor_position(current_position-1)

    def move_to_new_line(self):
        """
        Move to new line
        """
        self.type_text("\n")

    @property
    def ratio_width(self):
        return self._ratio_width

    @ratio_width.setter
    def ratio_width(self, value):
        self._ratio_width = value
        self.set_width(unit.w(value))

    @property
    def ratio_height(self):
        return self._ratio_height

    @ratio_height.setter
    def ratio_height(self, value):
        self._ratio_height = value
        self.set_height(unit.h(value))
        

class Key(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerKey"
    __gproperties__ = {
        "text": (
            GObject.TYPE_STRING,
            "key default text",
            "string appended to a text",
            " ",
            GObject.PARAM_READWRITE),
        "altgr_text": (
            GObject.TYPE_STRING,
            "altgr text",
            "altgr string appended to a text",
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

    def __init__(self):
        super().__init__()
        #self.set_size(dims.MENU_BUTTON_H_PX, dims.MENU_BUTTON_H_PX)
        self.connect("activate", self.on_activate)
        self.connect("notify::text", self._set_initial_label)

    def _set_initial_label(self, source, spec):
        self.set_default_label()
        self.disconnect_by_func(self._set_initial_label)

    def set_default_label(self):
        self.set_label(self.text)
        
    def set_swap_altgr_label(self):
        label = self.get_label()
        try:
            if self.altgr_text.lower() == label.lower():
                if label.islower():
                    # from lowercase altgr to lowercase default
                    self.set_label(self.text.lower())
                else:
                    # from uppercase altgr to (uppercase) default
                    self.set_label(self.text)
            else:     
                if label.isalpha() and self.altgr_text:
                    if self.get_label().islower():
                        # from lowercase default to lowercase altgr
                        self.set_label(self.altgr_text.swapcase())
                    else:
                        # from (uppercase) default to uppercase altgr
                        self.set_label(self.altgr_text)
        except AttributeError:
            return None

    def set_swap_caps_label(self):
        self.set_label(self.get_label().swapcase())

    def set_swap_special_label(self):
        try:
            if self.get_label() == self.special_text:
                self.set_default_label()
            else:
                self.set_special_label()
        except AttributeError:
            return None

    def set_special_label(self):
        self.set_label(self.special_text)

    def on_activate(self, source):
        if self.target:
            self.target.type_text(self.get_label())

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)

    @property
    def altgr_text(self):
        return self._altgr_text

    @altgr_text.setter
    def altgr_text(self, value):
        self._altgr_text = str(value)

    @property
    def special_text(self):
        return self._special_text

    @special_text.setter
    def special_text(self, value):
        self._special_text = str(value)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value


class Dictionary(GObject.GObject, pisak.widgets.PropertyAdapter):
    __gtype_name__ = "PisakSpellerDictionary"
    __gsignals__ = {
        "content_update":(
            GObject.SIGNAL_RUN_FIRST, None, ()),
        "processing_on":(
            GObject.SIGNAL_RUN_FIRST, None, ())
    }
    __gproperties__ = {
        "target": (
            Text.__gtype__,
            "target to follow",
            "id of text box to follow",
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.content = []

    def get_suggestion(self, accuracy_level):
        if accuracy_level < len(self.content): 
            return self.content[accuracy_level]
        
    def _update_content(self, *args):
        string = self.target.get_endmost_triplet()
        self.emit("processing-on")
        self.content = predictor.get_predictions(string)
        self.emit("content-update")

    def _follow_target(self):
        if self.target:
            text_field = self.target.clutter_text
            text_field.connect("text-changed", self._update_content)

    def _stop_following_target(self):
        try:
            if self.target:
                text_field = self.target.clutter_text
                text_field.disconnect_by_func("text-changed", self._update_content)
        except AttributeError:
            return None

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._stop_following_target()
        self._target = value
        self._follow_target()
        

class Prediction(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerPrediction"
    __gproperties__ = {
        "dictionary": (
            Dictionary.__gtype__,
            "prediction dictionary",
            "dictionary to get the suggested words from",
            GObject.PARAM_READWRITE),
        "order_num": (
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
        super().__init__()
        #self.set_size(dims.MENU_BUTTON_W_PX, dims.MENU_BUTTON_H_PX)
        self.connect("activate", self._on_activate)
        self.idle_icon_name = "hourglass"
        self.idle_icon_size = 50

    def _on_activate(self, source):
        label = self.get_label()
        if label and self.target:
            self.target.replace_endmost_string(label)

    def _update_button(self, source):
        try:
            if self.icon_name:
                self.icon_name = ""
        except AttributeError:
            pass
        new_label = self.dictionary.get_suggestion(self.order_num-1)
        if new_label:
            self.set_label(new_label)
            if self.get_disabled():
                self.set_disabled(False)
        else:
            self.set_label("")
            self.set_disabled(True)

    def _button_idle(self, source):
        self.set_label(" ")
        self.icon_size = self.idle_icon_size
        self.icon_name = self.idle_icon_name
        self.set_disabled(True)

    def _follow_dictionary(self):
        if self.dictionary:
            self.dictionary.connect("content-update", self._update_button)
            self.dictionary.connect("processing-on", self._button_idle)

    def _stop_following_dictionary(self):
        try:
            if self.dictionary:
                self.dictionary.disconnect_by_func("text-changed", self._update_button)
                self.dictionary.disconnect_by_func("processing-on", self._button_idle)
        except AttributeError:
            return None

    @property
    def dictionary(self):
        return self._dictionary

    @dictionary.setter
    def dictionary(self, value):
        self._stop_following_dictionary()
        self._dictionary = value
        self._follow_dictionary()

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def order_num(self):
        return self._order_num

    @order_num.setter
    def order_num(self, value):
        self._order_num = value
