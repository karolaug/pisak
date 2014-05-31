import sys
from gi.repository import Clutter, Mx
from pisak import switcher_app
import pisak.speller.widgets  # @UnusedImport
import pisak.layout  # @UnusedImport


script = None
dispatcher = None


class Dispatcher(object):
    MODEL = {
        "document": "concept/sample.txt"
    }
    
    def __init__(self):
        self._init_elements()
        self._init_func_dict()
        self._connect_menu_buttons(script.list_objects())

    def _init_elements(self):
        self.text_field = script.get_object("text_box")
        self.prediction_panel = script.get_object("prediction_panel")
        self.keyboard_panel = script.get_object("keyboard_panel")

    def _init_func_dict(self):
        self.MENU_FUNCS = {
            "go_to_keyboard": self.go_to_keyboard,
            "go_to_prediction": self.go_to_prediction,
            "go_to_main_menu": self.go_to_main_menu,
            "exit": self.exit_app,
            "save": self.save,
            "load": self.load,
            "print": self.print_doc,
            "send": self.send,
            "new_document": self.new_document,
            "default_chars": self.default_chars,
            "swap_altgr_chars": self.swap_altgr_chars,
            "swap_caps_chars": self.swap_caps_chars,
            "special_chars": self.special_chars,
            "text_to_speech": self.text_to_speech,
            "backspace": self.backspace,
            "space": self.space
        }
        
    def _connect_menu_buttons(self, objects):
        for item in objects:
            if item.__gtype_name__ == "PisakSpellerButton":
                value = item.get_property("speller-function")
                item.connect("activate", self.MENU_FUNCS[value])

    def go_to_keyboard(self, source):
        raise NotImplementedError

    def go_to_prediction(self, source):
        raise NotImplementedError

    def go_to_main_menu(self, source):
        raise NotImplementedError

    def exit_app(self, source):
        raise NotImplementedError

    def save(self, source):
        text = self.text_field.get_text()
        if text:
            with open(self.MODEL["document"], "w") as file:
                file.write(text)

    def load(self, source):
        with open(self.MODEL["document"], "r") as file:
            text = file.read()
        self.text_field.clear_all()
        self.text_field.type_text(text)

    def print_doc(self, source):
        raise NotImplementedError

    def send(self, source):
        raise NotImplementedError

    def new_document(self, source):
        self.text_field.clear_all()

    def default_chars(self, source):
        for item in self.keyboard_panel.get_children():
            if item.__gtype_name__ == "PisakSpellerKey":
                item.set_default_label()
            else:
                for sub_item in item.get_children():
                    sub_item.set_default_label()
        func = "special_chars"
        source.set_property("speller-function", func)
        source.connect("activate", self.MENU_FUNCS[func])
        source.set_default_label()

    def swap_altgr_chars(self, source):
        for item in self.keyboard_panel.get_children():
            if item.__gtype_name__ == "PisakSpellerKey":
                item.set_swap_altgr_label()
            else:
                for sub_item in item.get_children():
                    sub_item.set_swap_altgr_label()

    def swap_caps_chars(self, source):
        for item in self.keyboard_panel.get_children():
            if item.__gtype_name__ == "PisakSpellerKey":
                item.set_swap_caps_label()
            else:
                for sub_item in item.get_children():
                    sub_item.set_swap_caps_label()

    def special_chars(self, source):
        for item in self.keyboard_panel.get_children():
            if item.__gtype_name__ == "PisakSpellerKey":
                item.set_special_label()
            else:
                for sub_item in item.get_children():
                    sub_item.set_special_label()
        func = "default_chars"
        source.set_property("speller-function", func)
        source.connect("activate", self.MENU_FUNCS[func])
        source.set_alternative_label()

    def text_to_speech(self, source):
        raise NotImplementedError

    def backspace(self, source):
        self.text_field.delete_char()

    def space(self, source):
        self.text_field.type_text(" ")
        

class PisakSpellerStage(Clutter.Stage):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self._load_script()
        self._init_dispatcher()

    def _load_script(self):
        Mx.Button() # workaround for GI loader
        global script
        script = Clutter.Script()
        script.load_from_file(SCRIPT_PATH)
        self.view_actor = script.get_object("main")
        self.set_layout_manager(Clutter.BoxLayout())
        self.add_child(self.view_actor)

    def _init_dispatcher(self):
        global dispatcher
        dispatcher = Dispatcher()


class PisakSpellerApp(switcher_app.Application):
    """
    Pisak speller app with pisak speller stage.
    """
    def create_stage(self, argv):
        stage = PisakSpellerStage(self.context)
        stage.set_fullscreen(True)
        return stage
    

if __name__ == "__main__":
    SCRIPT_PATH = {
        "row": "pisak/speller/speller_row.json",
        "column": "pisak/speller/speller_column.json",
        "combined": "pisak/speller/speller_combined.json"
        }[sys.argv[1]]
    PisakSpellerApp(sys.argv).main()
