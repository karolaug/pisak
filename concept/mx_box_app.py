#!/usr/bin/env python3
from gi.repository import Clutter, Mx


class MyBoxLayout(Clutter.Actor):
    """
    Initial concept of custom BoxLayout widget
    """
    def __init__(self):
        super().__init__()
        self.set_layout_manager(Clutter.BoxLayout())
        self.set_background_color(Clutter.Color(255, 255, 255, 255))
        self.set_size(1, 1)


class ButtonStage(Clutter.Stage):
    def create_box_mx(self):
        return Mx.BoxLayout()

    def create_box_actor(self):
        box = Clutter.Actor()
        box.set_layout_manager(Clutter.BoxLayout())
        return box

    def create_box_custom(self):
        return MyBoxLayout()

    def __init__(self):
        super().__init__()

        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)

        # Uncomment one of these lines
        #self.box = self.create_box_actor()
        #self.box = self.create_box_mx()
        self.box = self.create_box_custom()

        self.box.set_x_expand(True)
        self.box.set_y_expand(True)
        self.add_child(self.box)

        self.button_a = Mx.Button()
        self.button_a.set_label("A")
        self.box.add_child(self.button_a)

        self.button_b = Mx.Button()
        self.button_b.set_label("B")
        self.button_b.set_x_expand(True)
        self.box.add_child(self.button_b)


def main():
    Clutter.init([])
    stage = ButtonStage()
    stage.connect("destroy", lambda _: Clutter.main_quit())
    stage.show_all()
    Clutter.main()


if __name__ == '__main__':
    main()