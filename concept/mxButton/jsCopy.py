#! /usr/bin/env python3


from gi.repository import Clutter, Mx

Clutter.init(None)

Mx.Style.get_default().load_from_file('tests.css')

script = Clutter.Script()
script.load_from_file('buttons.json')

stage = script.get_object('stage')

stage.show()

stage.connect('destroy', lambda *_ : Clutter.main_quit())
button = script.get_object('action-button')

action = button.get_property('action')

i = 0

def activate(a):
    global i
    i += 1
    a.set_property('display_name', 'Click {}'.format(i))
    a.set_property('icon', 'dialog-information')

def lab(b):
    b.set_property('label', 'Clicked')

action.connect('activated', activate)

button = script.get_object('custom-content')
button.connect('clicked', lab)

Clutter.main()
