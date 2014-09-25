"""
Main module of the symboler application. Launching and managing all the
application's views takes place here.
"""
from pisak import launcher, res


def prepare_symboler_view(stage, script, data):
    exit_button = script.get_object("button_exit")
    if exit_button is not None:
        exit_button.connect("clicked", lambda *_: stage.load_view(
            "main_panel/main", None))


VIEWS = {
    "symboler/main": (res.get("json/symboler/main.json"),
                     prepare_symboler_view)
}


if __name__ == "__main__":
    _symboler_app = {
        "views": VIEWS,
        "initial-view": "symboler/main",
        "initial-data": None
    }
    launcher.run(_symboler_app)
