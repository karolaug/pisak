#!/usr/bin/env python3
from gi.repository import Clutter


class MyButton(Clutter.Actor):
    def __init__(self):
        super().__init__()
        #self.set_label("Dont'click")
        self.set_background_color(Clutter.Color.new(64, 192, 64, 255))
        self.set_size(100, 100)
        self.connect("key-release-event", self.key_release)

    def key_release(self, *args):
        print("KEY RELEASE: BUTTON")
        # set focus to the stage
        self.get_stage().set_key_focus(self.get_stage())


class MyBox(Clutter.Actor):
    def __init__(self):
        super().__init__()
        self.connect("key-release-event", self.key_release)
        self.connect("notify::mapped", self.start_focus)
        self.button = MyButton()
        self.add_child(self.button)
        self.set_layout_manager(Clutter.BoxLayout())

    def start_focus(self, source, *args):
        # set focus to the box
        self.get_stage().set_key_focus(source)

    def key_release(self, source, *args):
        print("KEY RELEASE: BOX")
        # set focus to the button
        source.get_stage().set_key_focus(self.button)


class MyStage(Clutter.Stage):
    def __init__(self):
        super().__init__()
        self.box = MyBox()
        self.add_child(self.box)
        self.set_layout_manager(Clutter.BinLayout())


if __name__ == '__main__':
    Clutter.init([])
    stage = MyStage()
    stage.show()
    stage.connect("destroy", lambda _: Clutter.main_quit())
    Clutter.main()
