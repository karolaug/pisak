#!/usr/bin/python3

'''
Does button work?
'''
import sys
from pisak import switcher_app
from gi.repository import Clutter, Mx, Rsvg, Cogl

#Mx.Style.get_default().load_from_file('button.css')

class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        self.button = Mx.Button()

        self.script = Clutter.Script()
        self.script.load_from_file('concept/mxButton/button.json')

        self.button = self.script.get_object('button')

        self.icon = self.script.get_object('icon')

        handle = Rsvg.Handle()
        svg = handle.new_from_file('concept/mxButton/edytuj.svg')

        pixbuf = svg.get_pixbuf()

        pixbuf = pixbuf.scale_simple(100, 100, 3)

        self.icon.set_from_data(pixbuf.get_pixels(),Cogl.PixelFormat.RGBA_8888, pixbuf.get_width(), pixbuf.get_height(), pixbuf.get_rowstride())

        self.add_child(self.button)
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return ButtonStage()


if __name__ == '__main__':
    ButtonApp(sys.argv).main()
