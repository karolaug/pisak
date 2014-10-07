"""
Paint application main module
"""
import os
import logging

from pisak import launcher, res
from pisak.paint import widgets, handlers # @UnusedImport


def _set_easel_drawing_color(button, easel):
    easel.line_rgba = widgets.convert_color(button.get_background_color())


def _set_easel_line_width(button, easel):
    easel.line_width = int(button.get_label().split(" ")[0])


def prepare_paint_main_view(stage, script, data):
    easel = script.get_object("easel")
    button_start = script.get_object("button_start")
    if button_start and isinstance (button_start, widgets.Button):
        button_start.connect("clicked", easel.clean_up)
        button_start.connect("clicked", lambda *_: stage.load_view(
            "main_panel/main", None))
    for button in script.get_object("color_menu_box").get_children():
        if isinstance (button, widgets.Button):
            button.connect("clicked", _set_easel_drawing_color, easel)
    for button in script.get_object("line_menu_box").get_children():
        if isinstance (button, widgets.Button):
            button.connect("clicked", _set_easel_line_width, easel)

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
