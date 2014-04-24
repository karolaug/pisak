'''
Does content work?
'''
import sys
from pisak import switcher_app, unit
from gi.repository import Clutter


class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        self._init_bg()
        self._init_layout()


    def _init_bg_content(self):
        def draw_canvas(canvas, context, w, h):
            context.scale(w, h)
            context.set_line_width(0.2)
            context.set_source_rgba(1, 1, 1, 0.25)
            context.arc(0.5, 0.5, 0.45, 0, 6.3)
            context.stroke()
            return True
        background_image = Clutter.Canvas()
        background_image.set_size(unit.mm(4), unit.mm(4))
        background_image.connect("draw", draw_canvas)
        background_image.invalidate()
        self.bg.set_content(background_image)
        self.bg.set_content_repeat(Clutter.ContentRepeat.BOTH)
        self.bg.set_content_scaling_filters(Clutter.ScalingFilter.LINEAR, Clutter.ScalingFilter.LINEAR)
    
    def _init_bg(self):
        self.bg = Clutter.Actor()
        self.bg.set_background_color(Clutter.Color.new(0xcc, 0xcc, 0xcc, 0xFF))
        self.bg.set_x_expand(True)
        self.bg.set_y_expand(False)
        self.add_child(self.bg)
        self._init_bg_content()

    def _init_layout(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)




class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return ButtonStage()
        

if __name__ == '__main__':
    ButtonApp(sys.argv).main()