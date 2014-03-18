import sys
from gi.repository import Clutter, Mx
import unit
import widgets

class LibraryViewContents(Clutter.Actor):
    MODEL = {
        "items": [{"label": "Kategoria %d" % i, "image_path": "pisak_view/krolikarnia.jpg"} for i in range(8)]
    }
    def __init__(self):
        super(LibraryViewContents, self).__init__()
        self._init_elements()
        self.set_y_expand(True)
    
    def _init_elements(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_vertical(True)
        self.layout.set_spacing(30)
        self.scroll = widgets.PagedTileView()
        self.scroll.set_model(self.MODEL)

        self.scrollbar = Mx.ProgressBar()
        self.scrollbar.set_x_expand(True)
        page_ratio = 1. / self.scroll.page_count 
        self.scrollbar.set_progress(page_ratio)
        self.scrollbar.set_height(30)
        
        self.add_actor(self.scroll)
        self.add_actor(self.scrollbar)

    def update_scrollbar(self,progress):
        self.scrollbar.animatev(Clutter.AnimationMode.LINEAR, self.scroll.animation_speed, ['progress'],[progress])
    
    def next_page(self):
        self.scroll.next_page()
    

class LibraryView(Clutter.Actor):
    def __init__(self):
        super(LibraryView, self).__init__()
        self.set_clip_to_allocation(True)
        self._init_elements()
    
    def _init_elements(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.contents = LibraryViewContents()
        self.add_actor(self.contents)
        self.add_actor(PisakBackground())
    
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

