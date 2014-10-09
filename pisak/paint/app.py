"""
Paint application main module
"""
import os
import logging

from pisak import launcher, res
from pisak.paint import widgets, handlers # @UnusedImport


def prepare_paint_main_view(stage, script, data):
    easel = script.get_object("easel")
    button_start = script.get_object("button_start")
    if button_start is not None and isinstance (button_start, widgets.Button):
        button_start.connect("clicked", easel.clean_up)
        button_start.connect("clicked", lambda *_: stage.load_view(
            "main_panel/main", None))


VIEWS = {
    "paint/main": (res.get("json/paint/main.json"), prepare_paint_main_view)
}


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    _paint_app = {
        "views": VIEWS,
        "initial-view": "paint/main",
        "initial-data": None
    }
    launcher.run(_paint_app)
