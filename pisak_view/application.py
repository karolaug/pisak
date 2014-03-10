import sys
from gi.repository import Clutter, Mx
import unit

class VignetteShader(Clutter.ShaderEffect):
    pass    


class CategoryTile(Clutter.Actor):
    def __init__(self, category):
        super(CategoryTile, self).__init__()
        self.category = category
        self._init_elements()
        
    def _init_elements(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_vertical(True)
        self.preview = Mx.Image()
        self.preview.set_from_file("/home/piwaniuk/Obrazy/krolikarnia.jpg")
        self.preview.set_scale_mode(Mx.ImageScaleMode.FIT)
        self.label = Mx.Label()
        self.label.set_text(self.category)
        self.add_actor(self.preview)
        self.add_actor(self.label)
        

class LibraryScroll(Clutter.Actor):
    def __init__(self):
        super(LibraryScroll, self).__init__()
        self.categories = ["Kategoria %d" % i for i in range(12)]
        self.page = 0
        self.page_count = int((len(self.categories) + (6 // 2)) // 6)
        self._init_tiles()
        self.set_x_expand(True)
        self.set_y_expand(True)
        margin = Clutter.Margin()
        margin.left = margin.right = unit.mm(12)
        self.set_margin(margin)
    
    def _init_tiles(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.pop_out = Clutter.Actor()
        self.add_actor(self.pop_out)
        self.page_actor = self.generate_page(self.page)
        self.add_actor(self.page_actor)
    
    def generate_page(self, page):
        page_actor = Clutter.Actor()
        page_layout = Clutter.GridLayout()
        page_actor.set_layout_manager(page_layout)
        page_layout.set_row_spacing(unit.mm(12))
        page_layout.set_column_spacing(unit.mm(12))
        for i in range(2):
            for j in range(3):
                index = int(page * 6 + i * 3 + j)
                if index < len(self.categories):
                    tile = CategoryTile(self.categories[index])
                    page_layout.attach(tile, j, i, 1, 1)
        page_actor.set_size(self.get_width(), self.get_height())
        page_actor.set_x_expand(True)
        page_actor.set_y_expand(True)
        #page_actor.set_x(1366 - self.get_x())
        return page_actor
    
    @staticmethod
    def slide_in(page_actor):
        #page_actor.animatev(Clutter.AnimationMode.EASE_IN_OUT_QUAD, 1000, ["x"], [0])
        page_actor.set_x(0)
    
    @staticmethod    
    def slide_out(page_actor):
        page_actor.animatev(Clutter.AnimationMode.EASE_IN_OUT_QUAD, 1000, ["x"], [-1366])
    
    def next_page(self):
        self.page = (self.page + 1) % self.page_count
        new_page_actor = self.generate_page(self.page)
        
        #self.remove_actor(self.page_actor)
        self.add_actor(new_page_actor)
        self.slide_in(new_page_actor)
        self.slide_out(self.page_actor)
        #self.page_actor.destroy()
        self.page_actor = new_page_actor
    

class LibraryViewContents(Clutter.Actor):
    def __init__(self):
        super(LibraryViewContents, self).__init__()
        self._init_elements()
        self.set_y_expand(True)
    
    def _init_elements(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_vertical(True)
        self.scroll = LibraryScroll()
        self.scrollbar = Clutter.Texture.new_from_file("/home/piwaniuk/Obrazy/jagoda.jpg")
        self.scrollbar.set_height(20)
        self.add_actor(self.scroll)
        self.add_actor(self.scrollbar)
    
    def next_page(self):
        self.scroll.next_page()
        #self.scrollbar.update(self.scroll.get_page())
    

class LibraryView(Clutter.Actor):
    def __init__(self):
        super(LibraryView, self).__init__()
        self._init_elements()
    
    def _init_elements(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.add_actor(PisakBackground())
        self.contents = LibraryViewContents()
        self.add_actor(self.contents)
    
    def next_page(self):
        self.contents.next_page()


class PisakBackground(Clutter.Actor):
    def __init__(self):
        super(PisakBackground, self).__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.image = Clutter.Texture.new_from_file("hyperbolic_vignette.png")
        self.add_actor(self.image)


class PisakViewerButtons(Clutter.Actor):
    def __init__(self, viewer):
        super(PisakViewerButtons, self).__init__()
        self.viewer = viewer
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        self.button = Mx.Button()
        self.button.set_label(">>")
        self.button.set_y_expand(True)
        self.button.set_width(unit.mm(30))
        self.button.connect("clicked", lambda _: self.next_page())
        self.set_x_align(Clutter.ActorAlign.END)
        self.add_actor(self.button)

    def next_page(self):
        self.viewer.next_page()


class PisakViewerContainer(Clutter.Actor):
    def __init__(self):
        super(PisakViewerContainer, self).__init__()
        self._init_elements()
        margin = Clutter.Margin()
        margin.left = margin.right = margin.top = margin.bottom = unit.mm(12)
        self.set_margin(margin)
        
    def _init_elements(self):
        color_1 = Clutter.Color.new(128, 160, 224, 255)
        self.main = LibraryView()
        self.main.set_x_expand(True)
        self.main.set_y_expand(True)
        self.buttons = PisakViewerButtons(self)
        self.buttons.set_y_expand(False)
        self.buttons.set_x_expand(True)
        self.buttons.set_height(unit.mm(25))
        
        layout = Clutter.BoxLayout()
        layout.set_vertical(True)
        self.set_layout_manager(layout)
        layout.set_spacing(unit.mm(12))
        self.add_actor(self.main)
        self.add_actor(self.buttons)
     
    def next_page(self):
        self.main.next_page()


class PisakViewerStage(Clutter.Stage):
    def __init__(self):
        super(PisakViewerStage, self).__init__()
        self._init_elements()
    
    def _init_elements(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        #self.background = PisakBackground()
        #self.add_actor(self.background)
        self.contents = PisakViewerContainer()
        self.add_actor(self.contents)
    

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

