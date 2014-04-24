'''
Does content work?
'''
import sys
from pisak import switcher_app
from gi.repository import Clutter
from pisak.res import colors, dims

STRIPE_COUNT = 10

class Stripe(Clutter.Actor):
    def __init__(self):
        super().__init__()
        self.set_background_color(colors.BUTTON_BG)
        self.set_height(dims.MENU_BUTTON_H_PX)
        self.set_x_expand(True)

class GridStripes(Clutter.Actor):
    def __init__(self):
        super().__init__()
        self.set_x_expand(True)
        self._init_stripes()
        self.set_background_color(colors.TRANSPARENT)
        margin = Clutter.Margin()
        margin.top = margin.bottom = dims.H_SPACING_PX
        self.set_margin(margin)
    
    def _init_stripes(self):
        layout = Clutter.GridLayout()
        layout.set_row_spacing(dims.H_SPACING_PX)
        self.set_layout_manager(layout)
        for i in range(STRIPE_COUNT):
            actor = Stripe()
            layout.attach(actor, 1, i, 1, 1)

class BoxStripes(Clutter.Actor):
    def __init__(self):
        super().__init__()
        self.set_x_expand(True)
        self._init_stripes()
        self.set_background_color(colors.TRANSPARENT)
        margin = Clutter.Margin()
        margin.top = margin.bottom = dims.H_SPACING_PX
        self.set_margin(margin)
    
    def _init_stripes(self):
        layout = Clutter.BoxLayout()
        layout.set_spacing(dims.H_SPACING_PX)
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.set_layout_manager(layout)
        for _ in range(STRIPE_COUNT):
            actor = Stripe()
            self.add_child(actor)

class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        self._init_elements()
        self._init_layout()
    
    def _init_elements(self):
        self.grid_stripes = GridStripes()
        self.box_stripes = BoxStripes()
        self.add_child(self.grid_stripes)
        self.add_child(self.box_stripes)

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