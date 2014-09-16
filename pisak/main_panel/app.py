import os


def button_to_view(stage, script, button_name, stage_to_load, data=None):
    button = script.get_object(button_name)
    if button is not None:
        button.connect("clicked", lambda *_: stage.load_view(stage_to_load,
                                                             data))

def prepare_main_panel_view(stage, script, data):
    button_to_view(stage, script, "button_speller", "speller/main", None)
    button_to_view(stage, script, "button_viewer", "viewer/library", None)


def fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)


VIEWS = {
    "main_panel/main": (fix_path("main_panel.json"), prepare_main_panel_view)
}
