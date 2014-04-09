'''
Does button work?
'''
import sys
from pisak import switcher_app
from gi.repository import Clutter, Mx


class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        self.button = Mx.Button()
        self.button.set_label("Don't click")
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