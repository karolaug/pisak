"""
Paint application main module
"""
import os
import logging

from pisak import launcher
from pisak.paint import widgets, handlers # @UnusedImport


def _set_easel_color(button, easel):
    easel.rgba = _convert_color(button.get_background_color())


def _set_easel_line_width(button, easel):
    easel.line_width = int(button.get_label().split(" ")[0])

    
def _convert_color(clutter_color):
    rgba = ()
    string = clutter_color.to_string()
    for idx in range(1, 9, 2):
        rgba += (int(string[idx:idx+2], 16),)
    return rgba


def button_to_stage(stage, script, button_name, stage_to_load, data=None):
    button = script.get_object(button_name)
    if button is not None:
        button.connect("clicked", lambda *_: stage.load_view(stage_to_load,
                                                             data))

def prepare_paint_main_view(stage, script, data):
    button_to_stage(stage, script, "button_start", "main_panel/main")
    easel = script.get_object("easel")
    for button in script.get_object("color_menu_box").get_children():
        button.connect("clicked", _set_easel_color, easel)
    for button in script.get_object("line_menu_box").get_children():
        button.connect("clicked", _set_easel_line_width, easel)

def _fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)


VIEWS = {
    "paint/main": (_fix_path("paint.json"), prepare_paint_main_view)
}


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    _paint_app = {
        "views": VIEWS,
        "initial-view": "paint/main",
        "initial-data": None
    }
    launcher.run(_paint_app)
