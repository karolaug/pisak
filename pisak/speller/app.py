import os

from pisak import launcher


def prepare_speller_view(stage, script, data):
    exit_button = script.get_object("button_exit")
    if exit_button is not None:
        exit_button.connect("clicked", lambda *_: stage.load_view(
            "main_panel/main", None))


def fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)


VIEWS = {
    "speller/main": (fix_path("speller_combined.json"), prepare_speller_view)
}


_SPELLER_APP = {
    "views": {
        "speller/main": (fix_path("speller_combined.json"),
                         prepare_speller_view)
    },
    "initial-view": "speller/main",
    "initial-data": None
}


if __name__ == "__main__":
    launcher.run(_SPELLER_APP)
