#!/usr/bin/python3

import sys
from gi.repository import Rsvg, Gtk

class SvgWindow(Gtk.Window):

    def __init__(self, input_file):

        Gtk.Window.__init__(self, title='Edycja SVG poprzez CSS')
        self.set_border_width(0)
        self.input_file = input_file

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.handle = Rsvg.Handle()
        self.image = Gtk.Image()
        svg = self.handle.new_from_file(self.input_file)
        self.image.set_from_pixbuf(svg.get_pixbuf())
        vbox.pack_start(self.image, True, True, 0)

        button = Gtk.Button('Update')
        button.connect('clicked', self.on_click)
        vbox.pack_start(button, True, True, 0)

    def on_click(self, event):

        svg = self.handle.new_from_file(self.input_file)
        self.image.set_from_pixbuf(svg.get_pixbuf())
        return True

if __name__ == '__main__':
    try:
        inputfile = sys.argv[1]
    except IndexError:
        inputfile = 'concept/svg/edytuj.svg'

    win = SvgWindow(inputfile)
    win.connect("delete-event", Gtk.main_quit)
    win.show_all()
    Gtk.main()
