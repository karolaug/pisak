from gi.repository import Clutter, Mx, Cogl
from PIL import ImageFilter as ImF, Image as Im
import sys
from pisak import unit, res
import random
import os.path

class Image(Clutter.Actor):
    MODEL = os.path.join(res.PATH, 'krolikarnia.jpg')
    PIXEL_FORMATS = {'RGB': Cogl.PixelFormat.RGB_888, 'L': Cogl.PixelFormat.A_8}
    def __init__(self):
        super(Image, self).__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self._init_elements()
        self.set_image_from_data()

    def _init_elements(self):
        self.image = Mx.Image()
        self.image.set_scale_mode(Mx.ImageScaleMode.FIT)
        self.add_child(self.image)
        self.original_photo = self.buffer = Im.open(self.MODEL)
        self.zoom_timer = None
        self.noise_timer = None

    def set_image_from_data(self):
        data = self.buffer.tostring()
        mode = self.PIXEL_FORMATS[self.buffer.mode]
        width, height = self.buffer.size[0], self.buffer.size[1]
        row_stride = len(data) / height
        self.image.set_from_data(data, mode, width, height, row_stride)
        
    def mirror(self, button, event):
        axis = [Im.FLIP_LEFT_RIGHT, Im.FLIP_TOP_BOTTOM]
        self.buffer = self.buffer.transpose(axis[random.randint(0, 1)])
        self.set_image_from_data()

    def grayscale(self, button, event):
        self.buffer = self.buffer.convert('L')
        self.set_image_from_data()
        
    def rotate(self, button, event):     
        self.buffer = self.buffer.rotate(90, resample=Im.AFFINE)
        self.set_image_from_data()

    def noise(self, button, event):
        if not self.noise_timer:
            self.noise_timer = Clutter.Timeline.new(200)
            self.noise_timer.set_repeat_count(50)
            self.noise_timer.connect('completed', self._noise_update)
            self.noise_timer.start()
        else:
            self.noise_timer.stop()
            self.noise_timer = None

    def _noise_update(self, event):
        level = 40
        bands = self.buffer.getbands()
        source = self.buffer.split()
        for idx in range(len(source)):
            if bands[idx] != 'A':
                out = source[idx].point(lambda i: i + random.uniform(-level, level))
                source[idx].paste(out, None)
        mode = self.buffer.mode
        self.buffer = Im.merge(mode, source)
        self.set_image_from_data()

    def _zoom_cycle(self, button, event):
        if not self.zoom_timer:
            self.zoom_timer = Clutter.Timeline.new(200)
            self.zoom_timer.set_repeat_count(35)
            self.zoom_timer.connect('completed', self.zoom)
            self.zoom_timer.start()
        else:
            self.zoom_timer.stop()
            self.zoom_timer = None

    def zoom(self, event):
        width, height = self.buffer.size[0], self.buffer.size[1]
        x0, y0 = width/50, height/50
        x1, y1 = width-x0, height-y0
        self.buffer = self.buffer.transform((width, height), Im.EXTENT, (x0, y0, x1, y1))
        self.set_image_from_data()

    def edges(self, button, event):
        self.buffer = self.buffer.filter(ImF.FIND_EDGES)
        self.set_image_from_data()

    def sepia(self, button, event):
        level = 50
        grayscale = self.buffer.convert('L')
        red = grayscale.point(lambda i: i + level*1.5)
        green = grayscale.point(lambda i: i + level)
        blue = grayscale.point(lambda i: i - level*0.5)
        source = self.buffer.split()
        source[0].paste(red, None)
        source[1].paste(green, None)
        source[2].paste(blue, None)
        mode = self.buffer.mode
        self.buffer = Im.merge(mode, source)
        self.set_image_from_data()

    def contour(self, button, event):
        self.buffer = self.buffer.filter(ImF.CONTOUR)
        self.set_image_from_data()
        
    def invert(self, button, event):
        self.buffer = self.buffer.point(lambda i: 255-i)
        self.set_image_from_data()

    def solarize(self, button, event):
        threshold = 80
        buffer = self.buffer.copy()
        grayscale = buffer.convert('L')
        out = buffer.point(lambda i: i>threshold and 255-i)
        mask = grayscale.point(lambda i: i>threshold and 255)
        buffer.paste(out, None, mask)
        self.buffer = buffer
        self.set_image_from_data()

    def original(self, button, event):
        self.buffer = self.original_photo
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
        buttons = {'rotate': ['obróć', self.image.rotate], 'mirror': ['lustro', self.image.mirror],
                   'invert': ['negatyw', self.image.invert], 'zoom': ['powiększenie', self.image._zoom_cycle],
                   'solarize': ['prześwietlenie', self.image.solarize], 'grayscale': ['skala szarości', self.image.grayscale],
                   'original': ['oryginał', self.image.original], 'exit': ['wyjście', self.exit_app],
                   'noise': ['szum', self.image.noise], 'edges': ['krawędzie', self.image.edges],
                   'contour': ['szkic', self.image.contour], 'sepia': ['sepia', self.image.sepia]}
        for b in reversed(sorted(buttons)):
            button = Mx.Button()
            button.set_label(buttons[b][0])
            button.set_size(unit.mm(50), unit.mm(12))
            self.add_actor(button)
            button.connect("button_release_event", buttons[b][1])

    def exit_app(self, button, event):
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
        self.add_actor(self.buttons)
        self.add_actor(self.image)

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
