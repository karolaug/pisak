'''
Does button work?
'''
import sys
from pisak import switcher_app, res
from gi.repository import Clutter, Mx
import os.path


class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        self.button = Mx.Button()
        self.style = Mx.Style()
        self.style.load_from_file(os.path.join(res.PATH, "style.css"))
        self.button.set_style(self.style)
        self.button.set_label("Don't click")
        print(self.button.list_properties())
        print(self.button.get_property("border_image"))
        self.add_child(self.button)
        #self.layout = Clutter.BinLayout()
        #self.set_layout_manager(self.layout)


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return ButtonStage()
        

if __name__ == '__main__':
    ButtonApp(sys.argv).main()