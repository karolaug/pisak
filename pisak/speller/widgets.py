'''
Definitions of widgets specific to speller applet
'''
from gi.repository import Clutter, Mx, GObject, Pango

from pisak import unit
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
    
class Text(Mx.Label, pisak.widgets.PropertyAdapter):
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

    def add_operation(self, operation):
        if len(self.history) == 0 or (not self.history[-1].compose(operation)):
            self.history.append(operation)
        operation.apply(self)
    
    def revert_operation(self):
        if len(self.history) > 0:
            operation = self.history.pop()
            operation.revert(self)
        
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


class Prediction(pisak.widgets.Button):
    __gtype_name__ = "PisakSpellerPrediction"
    __gproperties__ = {
        "dictionary": (
            GObject.TYPE_STRING,
            "prediction dictionary",
            "path to source of prediction words",
            "",
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
        self.target = None
        #self.set_size(dims.MENU_BUTTON_W_PX, dims.MENU_BUTTON_H_PX)
        self.connect("activate", self.on_activate)

    def follow_target(self):
        if self.target:
            text_field = self.target.clutter_text
            #text_field.connect("text-changed", self.update_button)

    def stop_following_target(self):
        try:
            if self.target:
                text_field = self.target.clutter_text
                #text_field.disconnect_by_func("text-changed", self.update_button)
        except AttributeError:
            return None
            
    def on_activate(self, source):
        if self.target:
            self.target.replace_endmost_string(self.get_label())

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
        self.stop_following_target()
        self._target = value
        self.follow_target()

    @property
    def order_num(self):
        return self._order_num

    @order_num.setter
    def order_num(self, value):
        self._order_num = value
