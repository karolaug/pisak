#!/usr/bin/python3

'''
Does button work?
'''
import sys
from pisak.pisak import switcher_app
from gi.repository import Clutter, Mx

#Mx.Style.get_default().load_from_file('button.css')

class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        self.button = Mx.Button()
        self.script = Clutter.Script()
        self.script.load_from_file('button.json')

        self.button = self.script.get_object('button')
        self.button.set_icon_name('inkscape')
        
        self.button2 = Mx.Button()
        self.button2 = self.script.get_object('button2')
        self.button2.set_icon_name('gparted')
        self.button2.set_icon_visible(True)
        self.button2.set_size(100, 100)

        self.add_child(self.button)
        self.add_child(self.button2)

        self.img = Mx.Image()
        self.img.set_from_file('proba.svg')

        self.add_child(self.img)

        self.layout = Clutter.BinLayout()
        self.button.set_position(0, 0)
        self.button2.set_position(500, 0)
        print(self.button.get_position())
        self.set_layout_manager(self.layout)


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return ButtonStage()
        

if __name__ == '__main__':
    ButtonApp(sys.argv).main()
