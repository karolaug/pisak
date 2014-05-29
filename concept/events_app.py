#!/usr/bin/env python3
import sys

from gi.repository import Clutter


# highlight handler
def hover(source, event):
    source.set_background_color(Clutter.Color.new(96, 224, 96, 255))


Clutter.init(sys.argv)

# init stage
stage = Clutter.Stage()

# issue occurs only in fullscreen
stage.set_fullscreen(True)

stage.set_layout_manager(Clutter.BoxLayout())
stage.connect("destroy", lambda _: Clutter.main_quit())

# create vertical stripes
for _ in range(8):
    actor = Clutter.Actor()
    
    actor.set_x_expand(True)
    actor.set_background_color(Clutter.Color.new(128, 128, 128, 255))
    actor.set_reactive(True)
    actor.connect("enter-event", hover)
    
    stage.add_child(actor)

# start the app
stage.show_all()
Clutter.main()
