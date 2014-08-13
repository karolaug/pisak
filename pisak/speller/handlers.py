import subprocess
import os

from pisak import signals
from pisak.speller import widgets, database_agent


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
    

@signals.registered_handler("speller/nav_word_backward")
def nav_word_backward(text_box):
    text_box.move_word_backward()


@signals.registered_handler("speller/nav_word_forward")
def nav_word_forward(text_box):
    text_box.move_word_forward()


@signals.registered_handler("speller/save")
def save(pop_up):
    file_overwrite_text = "WYBIERZ PLIK DO NADPISANIA"
    empty_text_box_text = "BRAK TEKSTU DO ZAPISANIA"
    save_success_text = "POMYŚLNIE ZAPISANO PLIK"
    text_box = pop_up.target
    files_limit = 9
    files = database_agent.get_text_files()
    if len(files) < files_limit:
        text = text_box.get_text()
        if text:
            name_length = 10
            name = text.strip()[:name_length] + "..."
            file_path = database_agent.insert_text_file(name)
            with open(file_path, "w") as file:
                file.write(text)
            pop_up.on_screen("save", save_success_text)
        else:
            pop_up.on_screen("save", empty_text_box_text)
    else:
        pop_up.on_screen("save", file_overwrite_text, files)


@signals.registered_handler("speller/load")
def load(pop_up):
    files_present_text = "WYBIERZ PLIK"
    no_files_present_text = "BRAK PLIKÓW DO WCZYTANIA"
    files = database_agent.get_text_files()
    if files:
        pop_up.on_screen("load", files_present_text, files)
    else:
        pop_up.on_screen("load", no_files_present_text)
    

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
    

@signals.registered_handler("speller/unset_toggled_state_on_select")
def unset_toggled_state_on_select(button):
    keyboard_panel = button.related_object
    key_bag = []
    _find_and_get_keys(keyboard_panel, key_bag)
    for key in key_bag:
        try:
            key.disconnect_by_func(unset_toggled_state)
        except TypeError:
            pass
        key.connect_object("clicked", unset_toggled_state, button)


@signals.registered_handler("speller/unset_toggled_state")
def unset_toggled_state(button):
    if button.get_toggled():
        button.set_toggled(False)
    try:
        keyboard_panel = button.related_object
        key_bag = []
        _find_and_get_keys(keyboard_panel, key_bag)
        for key in key_bag:
            try:
                key.disconnect_by_func(unset_toggled_state)
            except TypeError:
                pass
    except AttributeError:
        pass


@signals.registered_handler("speller/set_toggled_state")
def set_toggled_state(button):
    if not button.get_toggled():
    	button.set_toggled(True)
    

@signals.registered_handler("speller/switch_toggled_state")
def switch_toggled_state(button):
    if button.get_toggled():
        button.set_toggled(False)
    else:
        button.set_toggled(True)
        

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
            

def _find_and_get_keys(keyboard_item, key_bag):
    if isinstance(keyboard_item, widgets.Key):
        key_bag.append(keyboard_item)
    else:
        for sub_item in keyboard_item.get_children():
            _find_and_get_keys(sub_item, key_bag)
