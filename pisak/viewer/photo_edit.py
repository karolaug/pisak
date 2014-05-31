from gi.repository import Clutter, Mx, Cogl, GObject
from PIL import ImageFilter as ImF, Image as Im
import sys
from pisak import unit, res, cursor, widgets
from pisak.speller import widgets
import random
import os.path
import subprocess
import pisak.layout



class Image(Clutter.Actor):
    MODEL = os.path.join(res.PATH, 'zdjecie.jpg')
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
        
    def mirror(self, button):
        axis = [Im.FLIP_LEFT_RIGHT, Im.FLIP_TOP_BOTTOM]
        self.buffer = self.buffer.transpose(axis[random.randint(0, 1)])
        self.set_image_from_data()

    def grayscale(self, button):
        self.buffer = self.buffer.convert('L')
        self.set_image_from_data()
        
    def rotate(self, button):     
        self.buffer = self.buffer.rotate(90, resample=Im.AFFINE)
        self.set_image_from_data()

    def noise(self, button):
        if not self.noise_timer:
            self.noise_timer = Clutter.Timeline.new(200)
            self.noise_timer.set_repeat_count(50)
            self.noise_timer.connect('completed', self._noise_update)
            self.noise_timer.start()
        else:
            self.noise_timer.stop()
            self.noise_timer = None

    def _noise_update(self, signal_source):
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

    def _zoom_cycle(self, button):
        if not self.zoom_timer:
            self.zoom_timer = Clutter.Timeline.new(200)
            self.zoom_timer.set_repeat_count(35)
            self.zoom_timer.connect('completed', self.zoom)
            self.zoom_timer.start()
        else:
            self.zoom_timer.stop()
            self.zoom_timer = None

    def zoom(self, signal_source):
        width, height = self.buffer.size[0], self.buffer.size[1]
        x0, y0 = width/50, height/50
        x1, y1 = width-x0, height-y0
        self.buffer = self.buffer.transform((width, height), Im.EXTENT, (x0, y0, x1, y1))
        self.set_image_from_data()

    def edges(self, button):
        self.buffer = self.buffer.filter(ImF.FIND_EDGES)
        self.set_image_from_data()

    def sepia(self, button):
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

    def contour(self, button):
        self.buffer = self.buffer.filter(ImF.CONTOUR)
        self.set_image_from_data()
        
    def invert(self, button, event):
        self.buffer = self.buffer.point(lambda i: 255-i)
        self.set_image_from_data()

    def solarize(self, button):
        threshold = 80
        buffer = self.buffer.copy()
        grayscale = buffer.convert('L')
        out = buffer.point(lambda i: i>threshold and 255-i)
        mask = grayscale.point(lambda i: i>threshold and 255)
        buffer.paste(out, None, mask)
        self.buffer = buffer
        self.set_image_from_data()

    def original(self, button):
        self.buffer = self.original_photo
        self.set_image_from_data()

    def take_photo(self, button):
        subprocess.call(['python', os.path.join(res.PATH, 'take_photo.py')])
        self.original_photo = self.buffer = Im.open(self.MODEL)
        self.set_image_from_data()
        
        
class Buttons1(Clutter.Actor):
    STYLE = Mx.Style()
    STYLE.load_from_file(os.path.join(res.PATH, 'photo_edit.css'))

    def __init__(self, container, image):
        super(Buttons1, self).__init__()
        self.container = container
        self.image = image
        self.layout = Clutter.BoxLayout()
        self.layout.set_vertical(True)
        self.set_layout_manager(self.layout)
        self.set_y_align(Clutter.ActorAlign.CENTER)
        self._init_elements()

    def _init_elements(self):
        buttons = {'menu': ['menu', self.menu],
                   'snapshot' : ['zdjęcie', self.image.take_photo],
                   'rotate': ['obróć', self.image.rotate], 
                   'mirror': ['lustro', self.image.mirror],
                   #'invert': ['negatyw', self.image.invert], 
                   #'zoom': ['powiększenie', self.image._zoom_cycle],
                   'solarize': ['prześwietlenie', self.image.solarize]}
        for b in reversed(sorted(buttons)):
            button = Mx.Button()
            button.set_style(self.STYLE)
            button.set_label(buttons[b][0])
            button.set_size(unit.mm(100), unit.mm(50))
            self.add_actor(button)
            button.connect("clicked", buttons[b][1])

    def menu(self, a, b):
        self.get_parent().get_parent().get_parent().change_view('a', 'b', 'menu')

    def exit_app(self, button, event):
        self.container.exit_app()

class Buttons2(Clutter.Actor):
    STYLE = Mx.Style()
    STYLE.load_from_file(os.path.join(res.PATH, 'photo_edit.css'))

    def __init__(self, container, image):
        super(Buttons2, self).__init__()
        self.container = container
        self.image = image
        self.layout = Clutter.BoxLayout()
        self.layout.set_vertical(True)
        self.set_layout_manager(self.layout)
        self.set_y_align(Clutter.ActorAlign.CENTER)
        self._init_elements()

    def _init_elements(self):
        buttons = {'original': ['oryginał', self.image.original], 
                   #'exit': ['wyjście', self.exit_app],
                   #'noise': ['szum', self.image.noise], 
                   'edges': ['krawędzie', self.image.edges],
                   'contour': ['szkic', self.image.contour], 
                   'sepia': ['sepia', self.image.sepia],
                   'grayscale': ['skala szarości', self.image.grayscale]}

        for b in reversed(sorted(buttons)):
            button = Mx.Button()
            button.set_style(self.STYLE)
            button.set_label(buttons[b][0])
            button.set_size(unit.mm(100), unit.mm(50))
            self.add_actor(button)
            button.connect("clicked", buttons[b][1])

    def exit_app(self, button):
        self.container.exit_app()


class PisakViewerContainer(Clutter.Actor):
    def __init__(self, stage):
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
        self.buttons1 = Buttons1(self, self.image)
        self.buttons2 = Buttons2(self, self.image)
        self.buttons1.set_y_expand(True)
        self.buttons2.set_y_expand(True)
        self.add_actor(self.buttons1)
        self.add_actor(self.image)
        self.add_actor(self.buttons2)

    def exit_app(self):
        self.stage.exit_app()

class PisakMainWindow(Clutter.Actor):
    
    def __init__(self):
        self.style = Mx.Style.get_default()
        self.style.load_from_file(os.path.join(res.PATH, "photo_edit.css"))
        super(PisakMainWindow, self).__init__()
        self.layout = Clutter.GridLayout()
        self.layout.set_column_spacing(10)
        self.layout.set_row_spacing(10)
        #layout.set_orientation(Clutter.Orientation.HORIZONTAL)
        self.set_layout_manager(self.layout)
        self.init_buttons()
        
    def init_buttons(self):
        self.SpellerButton = Mx.Button()
        self.SpellerButton.set_label('Speller')
        self.SpellerButton.set_size(300, 200)
        self.SpellerButton.set_name("speller")
        self.layout.attach(self.SpellerButton, 0, 0, 2, 1)
        
        self.EditButton = Mx.Button()
        self.EditButton.set_label('Edycja Zdjęcia')
        self.EditButton.set_name("edit")
        self.EditButton.set_size(300, 200)

        self.PisakLogo = Mx.Image()
        self.PisakLogo.set_scale_mode(1)
        self.PisakLogo.set_from_file(os.path.join(res.PATH, 
                                                  'logo_pisak.png'))
        
        self.NCBiRActor = Clutter.Actor()
        layout = Clutter.BoxLayout()
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.NCBiRActor.set_layout_manager(layout)
        
        self.NCBiRLabel = Mx.Label()
        self.NCBiRLabel.set_text('Dofinansowane ze środków:')
        self.NCBiRLogo = Mx.Image()
        self.NCBiRLogo.set_scale_mode(1)
        self.NCBiRLogo.set_from_file(os.path.join(res.PATH, 
                                                  'logo_ncbir.png'))
        self.NCBiRActor.add_actor(self.NCBiRLabel)
        self.NCBiRActor.add_actor(self.NCBiRLogo)


        self.OzarLogo = Mx.Image()
        self.OzarLogo.set_scale_mode(1)
        self.OzarLogo.set_from_file(os.path.join(res.PATH, 
                                                 'logoOzarowska.jpg'))

        self.BezSlowLogo = Mx.Image()
        self.BezSlowLogo.set_scale_mode(1)
        self.BezSlowLogo.set_from_file(os.path.join(res.PATH, 
                                                    'logo_bezSlow.jpg'))
            
        self.FuwLogo = Mx.Image()
        self.FuwLogo.set_scale_mode(1)
        self.FuwLogo.set_from_file(os.path.join(res.PATH, 
                                                'logowfuworyg.jpg'))

        self.BTLogo = Mx.Image()
        self.BTLogo.set_scale_mode(1)
        self.BTLogo.set_from_file(os.path.join(res.PATH, 
                                               'bt_logo.png'))

        #self.layout.attach(self.SpellerButton, 0, 0, 2, 1) #comment for edit
        self.layout.attach(self.SpellerButton, 0, 0, 1, 1) #uncomment for edit
        self.layout.attach(self.EditButton, 1, 0, 1, 1) #uncomment for edit
        self.layout.attach(self.NCBiRActor, 1, 3, 1, 1)
        self.layout.attach(self.PisakLogo, 0, 3, 1, 1)
        self.layout.attach(self.BTLogo, 1, 1, 1, 1)
        self.layout.attach(self.FuwLogo, 0, 1, 1, 1)
        self.layout.attach(self.OzarLogo, 0, 2, 1, 1)
        self.layout.attach(self.BezSlowLogo, 1, 2, 1, 1)

    def exit_app(self):
        self.stage.exit_app()

class PisakSpeller(object):
    def __init__(self):
        self.style = Mx.Style.get_default()
        self.style.load_from_file(os.path.join(res.PATH, "photo_edit.css"))

        Mx.Button()
        self.script = Clutter.Script()
        self.script.load_from_file(os.path.join(res.PATH, "speller_combined.json"))
        self.actor = self.script.get_object("main")
        self.text_box = self.script.get_object("text_box")
        self.clutter_text = self.text_box.get_clutter_text()
        self.clutter_text.set_line_wrap_mode(1)
        self.clutter_text.set_line_wrap(True)
        self.clutter_text.set_max_length(28)
        self.clutter_text.set_size(60, 300)

        self.space = self.script.get_object("key_3_9")
        self.space.connect("clicked", self.gap)

        self.backspace = self.script.get_object("key_3_8")
        self.backspace.connect("clicked", self.back)

    def gap(self, source):
        text = self.text_box.get_text()
        self.text_box.set_text(text + " ")

    def back(self, source):
        text = self.text_box.get_text()
        self.text_box.set_text(text[:-1])
        
class PisakViewerStage(Clutter.Stage):

    def __init__(self):
        super(PisakViewerStage, self).__init__()
        self._init_elements()
        self.set_layout_manager(Clutter.BinLayout())
    
    def _init_elements(self):
        self.contents = cursor.Group()
        self.contents.set_x_expand(True)
        self.contents.set_y_expand(True)
        #self.contents.set_background_color(Clutter.Color.new(255, 0, 0, 255))
        self.PisakImageEdit = PisakViewerContainer(self)
        pisakspeller = PisakSpeller()
        self.PisakSpeller = pisakspeller.actor
        self.PisakMainWindow = PisakMainWindow()
        self.PisakMainWindow.SpellerButton.connect("clicked", 
                                                   self.change_view, 
                                                   "speller")
        self.PisakMainWindow.EditButton.connect("clicked", 
                                                self.change_view, 
                                                "photo-edit")
        self.contents.add_actor(self.PisakMainWindow)
        self.current_view = self.PisakMainWindow
        self.add_actor(self.contents)

        self.mainWindowButton = pisakspeller.script.get_object("key_3_10")
        self.mainWindowButton.connect("clicked", self.change_view, "menu")

    def change_view(self, source, view):
        dic = {"speller" : self.PisakSpeller, 
               "photo-edit" : self.PisakImageEdit,
               "menu" : self.PisakMainWindow}
        self.contents.remove_child(self.current_view)
        #self.contents = cursor.Group()
        #self.remove_all_children()
        self.current_view = dic[view]
        self.contents.add_child(dic[view])
        self.contents.buttons = None
        #self.contents.buttons = None
        #self.contents.scan_buttons()
        #self.add_actor(self.contents)

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
