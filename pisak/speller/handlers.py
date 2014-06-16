from pisak.speller import widgets  # @UnusedImport

MODEL = {
        "document": "concept/sample.txt"
    }

def go_to_keyboard(keyboard_group):
    keyboard_group.start_cycle()

def go_to_prediction(prediction_group):
    prediction_group.start_cycle()

def go_to_main_menu(main_menu_group):
    main_menu_group.start_cycle()

def exit_app(*args):
    raise NotImplementedError

def save(text_box):
    text = text_box.get_text()
    if text:
        with open(MODEL["document"], "w") as file:
            file.write(text)

def load(text_box):
    with open(MODEL["document"], "r") as file:
        text = file.read()
    text_box.clear_all()
    text_box.type_text(text)

def print_doc(text_box):
    raise NotImplementedError

def send(text_box):
    raise NotImplementedError

def new_document(text_box):
    text_box.clear_all()

def text_to_speech(text_box):
    raise NotImplementedError

def backspace(text_box):
    text_box.delete_char()

def space(text_box):
    text_box.type_text(" ")
        
def default_chars(keyboard_panel):
    for item in keyboard_panel.get_children():
        if not isinstance(item, widgets.Key):
            for sub_item in item.get_children():
                sub_item.set_default_label()
        else:
            item.set_default_label()

def special_chars(keyboard_panel):
    for item in keyboard_panel.get_children():
        if not isinstance(item, widgets.Key):
            for sub_item in item.get_children():
                sub_item.set_special_label()
        else:
            item.set_special_label()

def swap_altgr_chars(keyboard_panel):
    for item in keyboard_panel.get_children():
        if not isinstance(item, widgets.Key):
            for sub_item in item.get_children():
                sub_item.set_swap_altgr_label()
        else:
            item.set_swap_altgr_label()

def swap_caps_chars(keyboard_panel):
    for item in keyboard_panel.get_children():
        if not isinstance(item, widgets.Key):
            for sub_item in item.get_children():
                sub_item.set_swap_caps_label()
        else:
            item.set_swap_caps_label()
