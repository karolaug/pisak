#!/usr/bin/env python

from gi.repository import Gtk, GLib, Gdk
import threading
import time

def main():
    rows = 15
    cols = 20
    button_rows = []
    running = True

    def cycle_callback():
        current_row = 0
        while running:
            for button in button_rows[current_row]:
                button.get_style_context().add_class("hilite")
            time.sleep(1.0)
            for button in button_rows[current_row]:
                button.get_style_context().remove_class("hilite")
            current_row = (current_row + 1) % rows

    style = Gtk.CssProvider()
    style.load_from_path("style.css")

    screen = Gdk.Screen.get_default()
    styleContext = Gtk.StyleContext()
    styleContext.add_provider_for_screen(screen, style, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    window = Gtk.Window()
    window.connect("destroy", lambda _: Gtk.main_quit())
    window.fullscreen()

    grid = Gtk.Grid()
    grid.set_row_spacing(4)
    grid.set_column_spacing(4)
    for i in range(rows):
        button_row = []
        for j in range(cols):
            button = Gtk.Button(label="(%d, %d)" % (i, j))
            button.set_vexpand(True)
            button.set_hexpand(True)
            button_row.append(button)
            grid.attach(button, j, i, 1, 1)
        button_rows.append(button_row)

    window.add(grid)

    window.show_all()

    threading.Thread(target=cycle_callback).start()
    GLib.threads_init()
    Gtk.main()
    running = False

main()
