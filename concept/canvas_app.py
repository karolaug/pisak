import sys
from pisak import switcher_app
from gi.repository import Clutter
import math
import time


class DynamicCanvas(Clutter.Actor):
    def __init__(self):
        super().__init__()
        self._canvas = Clutter.Canvas()
        self._canvas.set_size(640, 480)
        self.set_content(self._canvas)
        self._canvas.connect("draw", self._draw_canvas)
        self._canvas.invalidate()
        
    
    def _draw_canvas(self, canvas, context, width, height):
        context.set_source_rgba(1, 1, 1, 1)
        context.paint()
        context.set_source_rgba(0, 0, 0, 0.8)
        context.set_line_width(5)
        for i in range(30):
            context.move_to(0, 240 + 240 * math.sin(time.time() * (15 + i) / 30))
            context.line_to(640, 240 + 240 * math.sin(time.time()))
            
            context.move_to(640, 240 + 240 * math.sin(time.time() * (15 + i) / 30))
            context.line_to(0, 240 + 240 * math.sin(time.time()))
        context.stroke()
        return True
    
    def render(self):
        self._canvas.invalidate()


class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        self.dynamic_canvas = DynamicCanvas()
        self.dynamic_canvas.set_x_expand(True)
        self.dynamic_canvas.set_y_expand(True)
        self.add_child(self.dynamic_canvas)
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        Clutter.threads_add_timeout(0, 33, self._render, None)
    
    def _render(self, data):
        self.dynamic_canvas.render()
        return True


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return ButtonStage()


if __name__ == '__main__':
    ButtonApp(sys.argv).main()