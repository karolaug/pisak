import sys
from pisak import switcher_app
from gi.repository import Clutter, Mx, Gdk

class Stage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        self.button = Mx.Button()
        self.button.connect("clicked", self.move_cursor)
        
        self.display = Gdk.Display.get_default()
        self.screen = self.display.get_default_screen()

        self.add_child(self.button)
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.hide_cursor()

    def move_cursor(self, *args):
        self.display.warp_pointer(self.screen, 0, 0)


class App(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return Stage()
        

if __name__ == '__main__':
    App(sys.argv).main()
