from gi.repository import Clutter, Mx
import unit
import widgets

class LibraryView(Clutter.Actor):
    MODEL = {
        "items": [{"label": "Kategoria %d" % i, "image_path": "pisak_view/krolikarnia.jpg"} for i in range(20)],
        "page_interval": 6000
    }
    def __init__(self):
        super(LibraryView, self).__init__()
        self.set_clip_to_allocation(True)
        self._init_elements()
    
    def _init_elements(self):
        self._init_layout()
        self._init_content()
        self._init_overlay()
    
    def _init_layout(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        
    def _init_content(self):
        self.content = Clutter.Actor()
        self.add_child(self.content)
        self._init_content_layout()
        self._init_content_scroll()
        self._init_content_scrollbar()
    
    def _init_content_scrollbar(self):
        self.content_scrollbar = Mx.ProgressBar()
        self.content_scrollbar.set_x_expand(True)
        self.content_scrollbar.set_height(30)
        self.content.add_child(self.content_scrollbar)
    
    def _init_content_scroll(self):
        self.content_scroll = widgets.PagedTileView()
        self.content_scroll.set_model(self.MODEL)
        self.content_scroll.connect("page-changed", self.update_scrollbar)
        self.content_scroll.connect("page-selected", self.page_selected)
        self.content.add_child(self.content_scroll)
        
    def _init_content_layout(self):
        self.content_layout = Clutter.BoxLayout()
        self.content.set_layout_manager(self.content_layout)
        self.content_layout.set_vertical(True)
        self.content_layout.set_spacing(30)
    
    def _init_overlay(self):
        self.add_actor(Clutter.Texture.new_from_file("hyperbolic_vignette.png"))
    
    def next_page(self):
        self.content_scroll.next_page()
        
    def update_scrollbar(self, scroll, page):
        if page == -1:
            progress = 0.0
        elif scroll.page_count == 1:
            progress = 1.0
        else:
            progress = page / (scroll.page_count - 1.0)
        self.content_scrollbar.animatev(Clutter.AnimationMode.LINEAR, 500, ['progress'], [progress])
    
    def page_selected(self, scroll, page):
        print("Page selected:", page)
    
    def select(self):
        self.content_scroll.select()


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
    
    def select(self):
        self.main.select()


class PisakViewerStage(Clutter.Stage):
    def __init__(self):
        super(PisakViewerStage, self).__init__()
        self._init_elements()
        self.connect("key-release-event", self.key_release)
    
    def key_release(self, source, event):
        if event.keyval == 0x20:
            self.contents.select()
    
    def _init_elements(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
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

