import os

from pisak.main_panel import widgets
from pisak import launcher, res


def button_to_view(stage, script, button_name, stage_to_load, data=None):
    button = script.get_object(button_name)
    if button is not None:
        button.connect("clicked", lambda *_: stage.load_view(stage_to_load,
                                                             data))

def prepare_main_panel_view(stage, script, data):
    button_to_view(stage, script, "button_speller", "speller/main", None)
    button_to_view(stage, script, "button_viewer", "viewer/library", None)


def _fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)


VIEWS = {
    "main_panel/main": (res.get("json/main_panel/main_panel.json"), prepare_main_panel_view)
}


if __name__ == "__main__":
    _main_panel_app = {
        "views": VIEWS,
        "initial-view": "main_panel/main",
        "initial-data": None
    }
    launcher.run(_main_panel_app)
