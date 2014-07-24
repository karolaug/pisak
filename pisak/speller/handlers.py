from pisak import signals
from pisak.speller import widgets

MODEL = {
        "document": "concept/sample.txt"
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
def exit_app(*args):
    raise NotImplementedError

@signals.registered_handler("speller/undo")
def undo(*args):
    raise NotImplementedError

@signals.registered_handler("speller/nav_right") 
def nav_right(text_box):
    text_box.move_cursor_forward()

@signals.registered_handler("speller/nav_left") 
def nav_left(text_box):
    text_box.move_cursor_backward()

@signals.registered_handler("speller/save") 
def save(text_box):
    text = text_box.get_text()
    if text:
        with open(MODEL["document"], "w") as file:
            file.write(text)

@signals.registered_handler("speller/load") 
def load(text_box):
    with open(MODEL["document"], "r") as file:
        text = file.read()
    text_box.clear_all()
    text_box.type_text(text)

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
    raise NotImplementedError

@signals.registered_handler("speller/backspace") 
def backspace(text_box):
    text_box.delete_char()

@signals.registered_handler("speller/space") 
def space(text_box):
    text_box.type_text(" ")

@signals.registered_handler("speller/default_chars") 
def default_chars(keyboard_panel):
    for item in keyboard_panel.get_children():
        if not isinstance(item, widgets.Key):
            for sub_item in item.get_children():
                sub_item.set_default_label()
        else:
            item.set_default_label()

@signals.registered_handler("speller/special_chars") 
def special_chars(keyboard_panel):
    for item in keyboard_panel.get_children():
        if not isinstance(item, widgets.Key):
            for sub_item in item.get_children():
                sub_item.set_special_label()
        else:
            item.set_special_label()

@signals.registered_handler("speller/swap_altgr_chars") 
def swap_altgr_chars(keyboard_panel):
    for item in keyboard_panel.get_children():
        if not isinstance(item, widgets.Key):
            for sub_item in item.get_children():
                sub_item.set_swap_altgr_label()
        else:
            item.set_swap_altgr_label()

@signals.registered_handler("speller/swap_caps_chars") 
def swap_caps_chars(keyboard_panel):
    for item in keyboard_panel.get_children():
        if not isinstance(item, widgets.Key):
            for sub_item in item.get_children():
                sub_item.set_swap_caps_label()
        else:
            item.set_swap_caps_label()

@signals.registered_handler("speller/switch_label")
def switch_label(button):
    current_label = button.get_label()
    if not current_label:
        button.set_default_label()
    elif current_label == button.text:
        button.set_alternative_label()
    elif current_label == button.alternative_text:
        button.set_default_label()
