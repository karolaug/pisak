import os

from pisak import launcher, res


def prepare_speller_view(stage, script, data):
    exit_button = script.get_object("button_exit")
    if exit_button is not None:
        exit_button.connect("clicked", lambda *_: stage.load_view(
            "main_panel/main", None))


VIEWS = {
    "speller/main": (res.get("json/speller/speller_combined.json"),
                     prepare_speller_view)
}


if __name__ == "__main__":
    _speller_app = {
        "views": VIEWS,
        "initial-view": "speller/main",
        "initial-data": None
    }
    launcher.run(_speller_app)
