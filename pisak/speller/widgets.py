'''
Definitions of widgets specific to speller applet
'''
import threading

from gi.repository import Clutter, Mx, GObject, Pango

from pisak.speller.prediction import predictor
from pisak import unit, properties
import pisak.widgets


class Button(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerButton"

class CursorGroup(Clutter.Actor):
    __gtype_name__ = "PisakCursorGroup"

    def __init__(self):
        super().__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.connect("notify::mapped", self.init_content)
    
    def init_content(self, *args):
        self.text = [i for i in self.get_children() 
                     if type(i) == Text][0]
        self.init_cursor()
        self.text.clutter_text.connect('cursor_changed', self.move_cursor)

    def init_cursor(self):
        font_name = self.text.clutter_text.get_font_name()
        for i in font_name.split():
            try:
                self.cursor_height = unit.pt_to_px(int(i))
            except ValueError:
                if 'px' in i:
                    self.cursor_height = int(i.strip('px'))
                else:
                    pass
        self.cursor_height = round(self.cursor_height)
        self.cursor = Cursor((5, self.cursor_height))
        self.cursor.set_depth(10)
        self.add_child(self.cursor)
        self.cursor.set_x(0)
        self.cursor.set_y(0)
        
    def move_cursor(self, event):
        cursor_pos = self.text.clutter_text.get_cursor_position()
        coords = self.text.clutter_text.position_to_coords(cursor_pos)
        self.cursor.set_x(coords[1])
        self.cursor.set_y(coords[2])

class Cursor(Clutter.Actor):
    def __init__(self, size):
        super().__init__()

        self.width = size[0]
        self.height = size[1]
        self.set_size(self.width, self.height)

        self.canvas = Clutter.Canvas()
        self.canvas.set_size(self.width, self.height)
        self.canvas.connect('draw', self.draw)
        self.canvas.invalidate()
        self.set_content(self.canvas)

    @staticmethod
    def draw(canvas, context, width, height):
        context.set_source_rgb(0, 0, 0)
        context.rectangle(0, 0, width, height)
        context.fill()
        return True
    
class Text(Mx.Label, properties.PropertyAdapter):
    class Insertion(object):
        def __init__(self, pos, value):
            self.pos = pos
            self.value = value

        def apply(self, text):
            text.clutter_text.insert_text(self.value, self.pos)

        def revert(self, text):
            end = self.pos + len(self.value)
            text.clutter_text.delete_text(self.pos, end)

        def compose(self, operation):
            if isinstance(operation, Text.Insertion):
                consecutive = self.pos + len(self.value) == operation.pos
                compatible = self.value[-1].isspace() or \
                    not operation.value[0].isspace()
                if consecutive and compatible:
                    self.value = self.value + operation.value
                    return True
                else:
                    return False
            else:
                return False

        def __str__(self):
            return "+ {} @ {}".format(self.value, self.pos)

    class Deletion(object):
        def __init__(self, pos, value):
            self.pos = pos
            self.value = value

        def apply(self, text):
            end = self.pos + len(self.value)
            text.clutter_text.delete_text(self.pos, end)

        def revert(self, text):
            text.clutter_text.insert_text(self.value, self.pos)

        def compose(self, operation): 
            if isinstance(operation, Text.Deletion):
                consecutive = operation.pos + len(operation.value) == self.pos
                compatible = operation.value[-1].isspace() or \
                    not self.value[0].isspace()
                if consecutive and compatible:
                    self.pos = operation.pos
                    self.value = operation.value + self.value
                    return True
                else:
                    return False
            else:
                return False

        def __str__(self):
            return "- {} @ {}".format(self.value, self.pos)

    class Replacement(object):
        def __init__(self, pos, before, after):
            self.pos = pos
            self.before = before
            self.after = after

        def _replace(self, text, before, after):
            text.clutter_text.delete_text(self.pos, self.pos + len(before))
            text.clutter_text.insert_text(self.pos, after)

        def apply(self, text):
            self._replace(text, self.before, self.after)

        def revert(self, text):
            self._replace(text)

        def compose(self):
            return False

        def __str__(self):
            return "{} -> {} @ {}".format(self.before, self.after, self.pos)

    __gtype_name__ = "PisakSpellerText"
    __gproperties__ = {
        "ratio_width": (GObject.TYPE_FLOAT, None, None, 0, 1., 0, GObject.PARAM_READWRITE),
        "ratio_height": (GObject.TYPE_FLOAT, None, None, 0, 1., 0, GObject.PARAM_READWRITE)}
    
    def __init__(self):
        super().__init__()
        self.history = []
        self.clutter_text = self.get_clutter_text()
        self._set_text_params()
        self.clutter_text.set_reactive(True)
        self.clutter_text.set_editable(True)
        self.line = 0

    def add_operation(self, operation):
        if len(self.history) == 0 or not self.history[-1].compose(operation):
            self.history.append(operation)
        operation.apply(self)
    
    def revert_operation(self):
        if len(self.history) > 0:
            self.history.pop().revert(self)
        
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
        operation = Text.Insertion(self.get_text_length(), text)
        self.add_operation(operation)

    def type_unicode_char(self, char):
        """
        Append the given unicode character to the text buffer
        @param char unicode character in the form of unicode escape sequence
        :deprecated:
        """ 
        # TODO: remove
        operation = Text.Insertion(self.get_text_length(), char)
        self.add_operation(operation)

    def delete_char(self):
        """
        Delete the endmost single character
        """
        pos = self.get_text_length() - 1
        text = self.get_text()[-1]
        operation = Text.Deletion(pos, text)
        self.add_operation(operation)
        
        #self.clutter_text.delete_text(pos, pos+1)

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
        operation = Text.Deletion(0, self.get_text())
        self.add_operation(operation)


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

    def replace_endmost_string(self, text_after):
        """
        Look for the first string of characters with no whitespaces starting
        from the end of the text buffer and replace it with the given text
        @param text string passed after a user's action
        """
        current_text = self.get_text()
        start_pos = current_text.rstrip().rfind(' ') + 1
        #end_pos = self.get_text_length()
        text_before = current_text[start_pos : -1]
        operation = Text.Replacement(start_pos, text_before, text_after)
        self.add_operation(operation)
        #self.delete_text(start_pos, end_pos)
        #self.type_text(text)

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
        text_length = self.get_text_length()
        if current_position > 0:
            self.clutter_text.set_cursor_position(current_position-1)
        elif current_position == -1 and text_length > 0:
            self.clutter_text.set_cursor_position(text_length-1)

    def move_line_up(self):
        """
        Move cursor one line up
        """
        
        layout = self.clutter_text.get_layout()
        text = self.get_text()
        cursor_pos = self.clutter_text.get_cursor_position()
        if cursor_pos == 0:
            index_ = 0
        else:
            index_ = len(text)

        line_no, x = layout.index_to_line_x(index_, 0)

        line_no -= 1
        if line_no < 0:
            return False

        if x_pos != -1:
            x = x_pos

        layout_line = layout.get_line_readonly(line_no)
        if not layout_line:
            return False

        index_, trailing = layout.x_to_index(layout_line, x)

        #pos = 

    def move_line_down(self):
        """
        Move cursor one line down
        """

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
        "default_text": (
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
        self.pre_special_text = None
        self.undo_chain = []
        self.allowed_undos = set()
        #self.set_size(dims.MENU_BUTTON_H_PX, dims.MENU_BUTTON_H_PX)
        self.connect("activate", self.on_activate)
        self.connect("notify::default-text", self._set_initial_label)

    def _set_initial_label(self, source, spec):
        self.set_default_label()
        self.disconnect_by_func(self._set_initial_label)

    def _cache_pre_special_text(self, text_to_cache):
        if not self.pre_special_text:
            self.pre_special_text = text_to_cache

    def undo_label(self):
        while self.undo_chain:
            operation = self.undo_chain.pop()
            if callable(operation) and operation in self.allowed_undos:
                operation(self)
        
    def set_pre_special_label(self):
        if self.pre_special_text:
            self.set_label(self.pre_special_text)
            self.pre_special_text = None

    def set_default_label(self):
        self.set_label(self.default_text)

    def set_special_label(self):
        self._cache_pre_special_text(self.get_label())
        self.set_label(self.special_text)

    def set_caps_label(self):
        label = self.get_label()
        if label.isalpha():
            self.set_label(label.upper())

    def set_lower_label(self):
        label = self.get_label()
        if label.isalpha():
            self.set_label(label.lower())

    def set_altgr_label(self):
        try:
            label = self.get_label()
            if label.isalpha():
                if label.islower():
                    self.set_label(self.altgr_text.lower())
                elif label.isupper():
                    self.set_label(self.altgr_text.upper())
        except AttributeError:
            return None
        
    def set_swap_altgr_label(self):
        try:
            label = self.get_label()
            if self.altgr_text.lower() == label.lower():
                if label.islower():
                    # from lowercase altgr to lowercase default
                    self.set_label(self.default_text.lower())
                else:
                    # from uppercase altgr to (uppercase) default
                    self.set_label(self.default_text.upper())
            else:
                if label.isalpha() and self.altgr_text:
                    if label.islower():
                        # from lowercase default to lowercase altgr
                        self.set_label(self.altgr_text.lower())
                    else:
                        # from (uppercase) default to uppercase altgr
                        self.set_label(self.altgr_text.upper())
        except AttributeError:
            return None

    def set_swap_caps_label(self):
        label = self.get_label()
        if label.isalpha():
            self.set_label(label.swapcase())

    def set_swap_special_label(self):
        try:
            if self.get_label() == self.special_text:
                self.set_pre_special_label()
            else:
                self.set_special_label()
        except AttributeError:
            return None

    def on_activate(self, source):
        if self.target:
            self.target.type_text(self.get_label())
        
    @property
    def default_text(self):
        return self._default_text

    @default_text.setter
    def default_text(self, value):
        self._default_text = str(value)

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


class Dictionary(GObject.GObject, properties.PropertyAdapter):
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
        self.lock = threading.Lock() #nessesary

    def get_suggestion(self, accuracy_level):
        if accuracy_level < len(self.content): 
            return self.content[accuracy_level]

    def do_prediction(self): #function to preform in a separate thread
        with self.lock: #might be replaced with clutter.threads_enter and clutter.threads_leave
            string = self.target.get_endmost_triplet()
            self.content = predictor.get_predictions(string)
        self.emit("content-update")

    def _update_content(self, *args):
        self.emit("processing-on")
        t = threading.Thread(target = self.do_prediction) #very simple solution, not sure
        t.daemon = True #thread will be killed when the main program is killed
        t.start()

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
            GObject.PARAM_READWRITE),
        "idle_icon_name": (
            GObject.TYPE_STRING,
            "idle icon name",
            "name of the icon on button while idle",
            " ",
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        #self.set_size(dims.MENU_BUTTON_W_PX, dims.MENU_BUTTON_H_PX)
        self.connect("activate", self._on_activate)
        self.idle_icon_name = "hourglass"
        self.icon_size = 50

    @property
    def idle_icon_name(self):
        return self._idle_icon_name

    @idle_icon_name.setter
    def idle_icon_name(self, value):
        self._idle_icon_name = value

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
            self.set_disabled(False)
        else:
            self.set_label("")
            self.set_disabled(True)

    def _button_idle(self, source):
        self.set_label(" ")
        try:
            self.icon_name = self.idle_icon_name
        except AttributeError:
            pass
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
