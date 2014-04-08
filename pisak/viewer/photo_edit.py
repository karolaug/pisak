from gi.repository import Clutter, Mx, Cogl
from PIL import ImageOps as ImO, Image as Im
import sys
import unit
import random


class Image(Clutter.Actor):
    MODEL = './pisak/res/krolikarnia.jpg'
    def __init__(self):
        super(Image, self).__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self._init_elements()
        self.set_image_from_data()

    def _init_elements(self):
        self.pixel_formats = {'RGB': Cogl.PixelFormat.RGB_888, 'L': Cogl.PixelFormat.A_8}
        self.image = Mx.Image()
        self.image.set_scale_mode(Mx.ImageScaleMode.FIT)
        self.add_child(self.image)
        self.buffer = Im.open(self.MODEL)

    def set_image_from_data(self):
        self.data = self.buffer.tostring()
        self.mode = self.pixel_formats[self.buffer.mode]
        self.width, self.height = self.buffer.size[0], self.buffer.size[1]
        self.row_stride = len(self.data) / self.height
        self.image.set_from_data(self.data, self.mode, self.width, self.height, self.row_stride)
        
    def mirror(self):
        axis = [Im.FLIP_LEFT_RIGHT, Im.FLIP_TOP_BOTTOM]
        self.buffer = self.buffer.transpose(axis[random.randint(0,1)])
        self.set_image_from_data()

    def grayscale(self):
        self.buffer = self.buffer.convert('L')
        self.set_image_from_data()
        
    def rotate(self):     
        self.buffer = self.buffer.rotate(90, resample=Im.AFFINE)
        self.set_image_from_data()

    def _zoom_cycle(self):
        if not hasattr(self, 'zoom_timer'):
            self.zoom_timer = Clutter.Timeline.new(200)
            self.zoom_timer.set_repeat_count(35)
            self.zoom_timer.connect('completed', lambda _: self.zoom())
            self.zoom_timer.start()
        else:
            self.zoom_timer.stop()
            delattr(self, 'zoom_timer')

    def zoom(self):
        x0, y0 = self.width/50, self.height/50
        x1, y1 = self.width-x0, self.height-y0
        self.buffer = self.buffer.transform((self.width, self.height),Im.EXTENT,(x0, y0, x1, y1))
        self.set_image_from_data()
        
    def invert(self):
        self.buffer = ImO.invert(self.buffer)
        self.set_image_from_data()

    def solarize(self):
        threshold = 80
        self.buffer = ImO.solarize(self.buffer, threshold)
        self.set_image_from_data()

    def original(self):
        self.buffer = Im.open(self.MODEL)
        self.set_image_from_data()
        
        
class Buttons(Clutter.Actor):
    def __init__(self, container, image):
        super(Buttons, self).__init__()
        self.container = container
        self.image = image
        self.layout = Clutter.BoxLayout()
        self.layout.set_vertical(True)
        self.set_layout_manager(self.layout)
        self.set_y_align(Clutter.ActorAlign.CENTER)
        self._init_elements()

    def _init_elements(self):
        self.buttons = {'obróć': self.image.rotate, 'lustro': self.image.mirror, 'negatyw': self.image.invert,
                        'powiększenie': self.image._zoom_cycle, 'prześwietlenie': self.image.solarize, 'skala szarości': self.image.grayscale,
                        'oryginał': self.image.original, 'wyjście': self.exit_app}
        for b in sorted(self.buttons):
            button = Mx.Button()
            button.set_label(b)
            button.set_size(unit.mm(50), unit.mm(25))
            self.add_actor(button)
            button.connect("button_release_event", lambda x,b=button: self.select(x,b))

    def select(self, button, x):
        label = button.get_label()
        self.buttons[label]()

    def exit_app(self):
        self.container.exit_app()


class PisakViewerContainer(Clutter.Actor):
    def __init__(self,stage):
        super(PisakViewerContainer, self).__init__()
        self.stage = stage
        self.set_x_expand(True)
        self.set_y_expand(True)
        layout = Clutter.BoxLayout()
        layout.set_vertical(False)
        self.set_layout_manager(layout)
        layout.set_spacing(unit.mm(10))
        margin = Clutter.Margin()
        margin.left = margin.right = margin.top = margin.bottom = unit.mm(12)
        self.set_margin(margin)
        self._init_elements()
        
    def _init_elements(self):
        self.image = Image()
        self.image.set_x_expand(True)
        self.image.set_y_expand(True)
        self.buttons = Buttons(self, self.image)
        self.buttons.set_y_expand(True)
        self.add_actor(self.image)
        self.add_actor(self.buttons)

    def exit_app(self):
        self.stage.exit_app()


class PisakViewerStage(Clutter.Stage):
    def __init__(self):
        super(PisakViewerStage, self).__init__()
        self._init_elements()
    
    def _init_elements(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.contents = PisakViewerContainer(self)
        self.add_actor(self.contents)

    def exit_app(self):
        self.destroy()
    

class PisakViewApp(object):
    def __init__(self, argv):
        PisakViewApp.APP = self
        Clutter.init(argv)
        self.stage = PisakViewerStage()
        self.stage.connect("destroy", lambda _: Clutter.main_quit())
        self.stage.set_fullscreen(True)
        self.stage.show_all()
    
    def main(self):
        Clutter.main()

PisakViewApp(sys.argv).main()
