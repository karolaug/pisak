'''
Does content work?
'''
import sys
from pisak import switcher_app, widgets
from gi.repository import Clutter
from pisak.res import colors, dims

class ViewActor(Clutter.Actor):
    def __init__(self):
        super().__init__()
        self.set_x_expand(True)
        self.set_y_expand(True)
        self.set_background_color(colors.TRANSPARENT)
        self._init_elements()

    def _init_elements(self):
        self._init_layout()
        self._init_content()

    def _init_layout(self):
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)

    def _init_content(self):
        self.menu = widgets.ButtonsMenu(None)
        self.menu.set_background_color(colors.BUTTON_BG)
        self.layout.attach(self.menu, 0, 0, 1, 2)
        #self.menu.set_size(50, 50)

        self.header = Clutter.Actor()
        self.header.set_background_color(colors.HILITE_1)
        self.layout.attach(self.header, 1, 0, 1, 1)
        self.header.set_height(dims.MENU_BUTTON_H_PX)
        self.header.set_x_expand(True)

        self.scroll = Clutter.Actor()
        self.scroll.set_background_color(colors.TRANSPARENT)
        self.layout.attach(self.scroll, 1, 1, 1, 1)
        self.scroll.set_y_expand(True)

        self.bar = Clutter.Actor()
        self.bar.set_background_color(colors.HILITE_1)
        self.layout.attach(self.bar, 0, 2, 2, 1)
        self.bar.set_height(dims.MENU_BUTTON_H_PX)
        self.set_x_expand(True)



class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        self._init_elements()
        self._init_layout()

    def _init_elements(self):
        self.view_actor = ViewActor()
        self.add_child(self.view_actor)

    def _init_layout(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        stage = ButtonStage()
        stage.set_fullscreen(True)
        return stage


if __name__ == '__main__':
    ButtonApp(sys.argv).main()