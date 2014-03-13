#!/usr/bin/env python3

from gi.repository import Clutter
import sys
import os.path
import model
import random

XDG_PHOTOS_DIR = "./obrazy"

class HiliteTile(Clutter.Actor):
    def __init__(self, photo_library):
        super(HiliteTile, self).__init__()    
        color = Clutter.Color.new(128, 160, 224, 255)
        self.base = Clutter.Rectangle.new_with_color(color)
        self.photo = Clutter.Texture.new_from_file(random.choice(list(photo_library.photos)).path)
        layout = Clutter.BinLayout.new(Clutter.BinAlignment.CENTER, Clutter.BinAlignment.CENTER)
        self.set_layout_manager(layout)
        self.add_actor(self.base)
        self.add_actor(self.photo)

def create_stage(XDG_PHOTOS_DIR):
    Clutter.init(sys.argv)

    stage = Clutter.Stage()
    
    
    library = None
    try:
        library = model.create_library(XDG_PHOTOS_DIR)
    except:
        library = model.Library(XDG_PHOTOS_DIR)
    
    library.scan()
    
    stage.photo_library = library
    stage.set_title("HW App")

    stage.set_color(Clutter.Color.new(64, 64, 64, 255))
    stage.connect("destroy", lambda _: Clutter.main_quit())
    return stage

def draw(stage):
    padding = 0.1
    rows = 3
    cols = 4
    w = (1 - padding) / cols
    x_pad = padding / (cols + 1)
    h = (1 - padding) / rows
    y_pad = padding / (rows + 1)

    for i in range(cols):
      for j in range(rows):
        x = i * w + (i + 1) * x_pad
        y = j * h + (j + 1) * y_pad
        rect = HiliteTile(stage.photo_library)
        rect.set_size(w * stage.get_width(), h * stage.get_height())
        rect.set_x(x * stage.get_width())
        rect.set_y(y * stage.get_height())
        Clutter.Container.add_actor(stage, rect)
    
def set_fullscreen(stage, cont):
    stage.connect("notify::allocation", cont)
    stage.set_fullscreen(True)

def main():
    stage = create_stage(XDG_PHOTOS_DIR)
    stage.show_all()
    set_fullscreen(stage, lambda _, __: draw(stage))
    Clutter.main()
    
main()
