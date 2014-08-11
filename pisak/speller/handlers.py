import subprocess
import os

from pisak import res, signals
from pisak.speller import widgets

MODEL = {
        "document": os.path.join(res.PATH, "sample.txt")
    }

@signals.registered_handler("speller/go_to_keyboard")
def go_to_keyboard(keyboard_group):
    keyboard_group.start_cycle()

@signals.registered_handler("speller/go_to_prediction")
def go_to_prediction(prediction_group):
    prediction_group.start_cycle()

@signals.registered_handler("speller/go_to_main_menu")
def go_to_main_menu(main_menu_group):
    main_menu_group.start_cycle()

@signals.registered_handler("speller/exit")
def exit_app(app):
    app.get_stage().destroy()

@signals.registered_handler("speller/undo")
def undo(text_box, *args):
    text_box.revert_operation()

@signals.registered_handler("speller/nav_right")
def nav_right(text_box):
    text_box.move_cursor_forward()

@signals.registered_handler("speller/nav_left")
def nav_left(text_box):
    text_box.move_cursor_backward()

@signals.registered_handler("speller/nav_up")
def nav_up(text_box):
    text_box.move_line_up()

@signals.registered_handler("speller/save")
def save(text_box):
    text = text_box.get_text()
    if text:
        with open(MODEL["document"], "w") as file:
            file.write(text)

@signals.registered_handler("speller/load")
def load(text_box):
    try:
        with open(MODEL["document"], "r") as file:
            text = file.read()
        text_box.clear_all()
        text_box.type_text(text)
    except FileNotFoundError:
        return None

@signals.registered_handler("speller/print")
def print_doc(text_box):
    raise NotImplementedError

@signals.registered_handler("speller/send")
def send(text_box):
    raise NotImplementedError

@signals.registered_handler("speller/new_document")
def new_document(text_box):
    text_box.clear_all()

@signals.registered_handler("speller/text_to_speech")
def text_to_speech(text_box):
    text = text_box.get_text()
    if text:
        subprocess.call(["milena_say", text])

@signals.registered_handler("speller/backspace")
def backspace(text_box):
    text_box.delete_char()

@signals.registered_handler("speller/space")
def space(text_box):
    text_box.type_text(" ")
    
@signals.registered_handler("speller/new_line")
def new_line(text_box):
    text_box.move_to_new_line()

@signals.registered_handler("speller/previous_chars")
def previous_chars(keyboard_item):
    if isinstance(keyboard_item, widgets.Key):
        keyboard_item.undo_label()
        try:
            keyboard_item.disconnect_by_func(previous_chars)
        except TypeError:
            return None
    else:
        for sub_item in keyboard_item.get_children():
            previous_chars(sub_item)

@signals.registered_handler("speller/default_chars")
def default_chars(keyboard_item):
    if isinstance(keyboard_item, widgets.Key):
        keyboard_item.set_default_label()
    else:
        for sub_item in keyboard_item.get_children():
            default_chars(sub_item)

@signals.registered_handler("speller/special_chars")
def special_chars(keyboard_item):
    if isinstance(keyboard_item, widgets.Key):
        keyboard_item.set_special_label()
        undo = widgets.Key.set_swap_special_label
        if undo not in keyboard_item.undo_chain:
            keyboard_item.undo_chain.append(undo)
    else:
        for sub_item in keyboard_item.get_children():
            special_chars(sub_item)

@signals.registered_handler("speller/altgr_chars")
def altgr_chars(keyboard_item):
    if isinstance(keyboard_item, widgets.Key):
        keyboard_item.set_altgr_label()
        undo = widgets.Key.set_swap_altgr_label
        if undo not in keyboard_item.undo_chain:
            keyboard_item.undo_chain.append(undo)
    else:
        for sub_item in keyboard_item.get_children():
            altgr_chars(sub_item)

@signals.registered_handler("speller/caps_chars")
def caps_chars(keyboard_item):
    if isinstance(keyboard_item, widgets.Key):
        keyboard_item.set_caps_label()
        undo = widgets.Key.set_lower_label
        if undo not in keyboard_item.undo_chain:
            keyboard_item.undo_chain.append(undo)
    else:
        for sub_item in keyboard_item.get_children():
            caps_chars(sub_item)

@signals.registered_handler("speller/lower_chars")
def lower_chars(keyboard_item):
    if isinstance(keyboard_item, widgets.Key):
        keyboard_item.set_lower_label()
        undo = widgets.Key.set_caps_label
        if undo not in keyboard_item.undo_chain:
            keyboard_item.undo_chain.append(undo)
    else:
        for sub_item in keyboard_item.get_children():
            lower_chars(sub_item)

@signals.registered_handler("speller/swap_special_chars")
def swap_special_chars(keyboard_item):
    if isinstance(keyboard_item, widgets.Key):
        keyboard_item.set_swap_special_label()
        keyboard_item.undo_chain.append(widgets.Key.set_swap_special_label)
    else:
        for sub_item in keyboard_item.get_children():
            swap_special_chars(sub_item)

@signals.registered_handler("speller/swap_altgr_chars")
def swap_altgr_chars(keyboard_item):
    if isinstance(keyboard_item, widgets.Key):
        keyboard_item.set_swap_altgr_label()
        keyboard_item.undo_chain.append(widgets.Key.set_swap_altgr_label)
    else:
        for sub_item in keyboard_item.get_children():
            swap_altgr_chars(sub_item)

@signals.registered_handler("speller/swap_caps_chars")
def swap_caps_chars(keyboard_item):
    if isinstance(keyboard_item, widgets.Key):
        keyboard_item.set_swap_caps_label()
        keyboard_item.undo_chain.append(widgets.Key.set_swap_caps_label)
    else:
        for sub_item in keyboard_item.get_children():
            swap_caps_chars(sub_item)

@signals.registered_handler("speller/lower_chars_on_select")
def lower_chars_on_select(keyboard_panel):
    _previous_chars_on_select(keyboard_panel, keyboard_panel, widgets.Key.set_lower_label)

@signals.registered_handler("speller/caps_chars_on_select")
def caps_chars_on_select(keyboard_panel):
    _previous_chars_on_select(keyboard_panel, keyboard_panel, widgets.Key.set_caps_label)

@signals.registered_handler("speller/swap_caps_chars_on_select")
def swap_caps_chars_on_select(keyboard_panel):
    _previous_chars_on_select(keyboard_panel, keyboard_panel, widgets.Key.set_swap_caps_label)

@signals.registered_handler("speller/swap_altgr_chars_on_select")
def swap_altgr_chars_on_select(keyboard_panel):
    _previous_chars_on_select(keyboard_panel, keyboard_panel, widgets.Key.set_swap_altgr_label)

@signals.registered_handler("speller/swap_special_chars_on_select")
def swap_special_chars_on_select(keyboard_panel):
    _previous_chars_on_select(keyboard_panel, keyboard_panel, widgets.Key.set_swap_special_label)

@signals.registered_handler("speller/switch_toggled_state_on_select")
def switch_toggled_state_on_select(button):
    pass#?????????????//
    #ustawic na wybranie a pozniej na wybranie key
    #switch tylko dla swap

@signals.registered_handler("speller/switch_toggled_state")
def switch_toggled_state(button):
    if button.style_pseudo_class_contains("toggled"):
        button.style_pseudo_class_remove("toggled")
    else:
        button.style_pseudo_class_add("toggled")

@signals.registered_handler("speller/switch_label")
def switch_label(button):
    button.switch_label()

@signals.registered_handler("speller/switch_icon")
def switch_icon(button):
    button.switch_icon()

def _previous_chars_on_select(keyboard_item, keyboard_panel, allowed_undo):
    if isinstance(keyboard_item, widgets.Key):
        try:
            keyboard_item.disconnect_by_func(previous_chars)
        except TypeError:
            pass
        keyboard_item.connect_object("clicked", previous_chars, keyboard_panel)
        keyboard_item.allowed_undos.add(allowed_undo)
    else:
        for sub_item in keyboard_item.get_children():
            _previous_chars_on_select(sub_item, keyboard_panel, allowed_undo)

def _find_and_get_keys(keyboard_item, keys_bag):
    if isinstance(keyboard_item, widgets.Key):
        keys_bag.append(keyboard_item)
    else:
        for sub_item in keyboard_item.get_children():
            _find_and_get_keys(sub_item)
