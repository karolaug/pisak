"""
Module defines classes specific to Viewer application.
"""
import os.path
from gi.repository import Clutter, Mx
from pisak import unit, view
from pisak import widgets
from pisak import switcher_app
from pisak import res

class LibraryView(Clutter.Actor):
    """
    Actor widget which presents categories in the photo library.
    """
    MODEL = {
        "items": [{
              "label": "Kategoria %d" % i,
              "image_path": os.path.join(res.PATH, "krolikarnia.jpg")
            } for i in range(20)
        ],
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
        self.content_scroll.connect("page-changed", self._update_scrollbar)
        self.content_scroll.connect("page-selected", self._page_selected)
        self.content.add_child(self.content_scroll)
        
    def _init_content_layout(self):
        self.content_layout = Clutter.BoxLayout()
        self.content.set_layout_manager(self.content_layout)
        self.content_layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.content_layout.set_spacing(30)
    
    def _init_overlay(self):
        background_path = os.path.join(res.PATH, "hyperbolic_vignette.png")
        self.add_child(Clutter.Texture.new_from_file(background_path))
    
    def next_page(self):
        """
        Force next page in view.
        """
        self.content_scroll.next_page()
        
    def _update_scrollbar(self, scroll, page):
        if page == -1:
            progress = 0.0
        elif scroll.page_count == 1:
            progress = 1.0
        else:
            progress = page / (scroll.page_count - 1.0)
        self.content_scrollbar.animatev(Clutter.AnimationMode.LINEAR, 500, ['progress'], [progress])
    
    def _page_selected(self, scroll, page):
        print("Page selected:", page)
    
    def select(self):
        """
        Force selection of current page.
        """
        self.content_scroll.select()
    
    def create_cycle(self):
        """
        Create a new cycle which is used by switcher to show consecutive pages from the model.
        """
        return self.content_scroll.create_cycle()


class PisakViewerButtons(Clutter.Actor):
    def __init__(self, viewer):
        """
        Widget of buttons associated with a LibraryView.
        @param viewer an instance of LibraryView
        """
        super(PisakViewerButtons, self).__init__()
        self.viewer = viewer
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        self.button = Mx.Button()
        self.button.set_label(">>")
        self.button.set_y_expand(True)
        self.button.set_width(unit.mm(30))
        self.button.connect("clicked", lambda _: self._next_page())
        self.set_x_align(Clutter.ActorAlign.END)
        self.add_child(self.button)

    def _next_page(self):
        """
        Signal handler.
        """
        self.viewer.next_page()

class PisakViewerContainer(Clutter.Actor):
    def __init__(self, context):
        """
        Application container, which creates other widgets.
        @param contect switcher application context passed from application
        """
        super(PisakViewerContainer, self).__init__()
        self.context = context
        self._init_elements()
        margin = Clutter.Margin()
        margin.left = margin.right = margin.top = margin.bottom = unit.mm(12)
        self.set_margin(margin)
        
    def _init_main(self):
        self.library_view = LibraryView()
        self.main = view.BasicViewContainer(self.context)
        self.main.push_view(self.library_view)
        self.main.set_x_expand(True)
        self.main.set_y_expand(True)

    def _init_elements(self):
        self._init_main()
        self.buttons = PisakViewerButtons(self)
        self.buttons.set_y_expand(False)
        self.buttons.set_x_expand(True)
        self.buttons.set_height(unit.mm(25))
        
        layout = Clutter.BoxLayout()
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.set_layout_manager(layout)
        layout.set_spacing(unit.mm(12))
        self.add_child(self.main)
        self.add_child(self.buttons)
     
    def next_page(self):
        """
        Force next page in the library view.
        """
        self.main.next_page()
    
    def select(self):
        """
        Force select current page in the library view.
        """
        self.main.select()
    
    def create_cycle(self):
        """
        Create new page-switching cycle in the library view
        """
        return self.library_view.create_cycle()


class PisakViewerStage(Clutter.Stage):
    def __init__(self, context):
        """
        Clutter stage which sets up the switcher application.
        @param context switcher application context passed from application
        """
        super(PisakViewerStage, self).__init__()
        self.context = context
        self._init_elements()
        self.context.switcher.push_cycle(self.content.create_cycle())
        self.input = switcher_app.KeyboardSwitcherInput(self)
        self.context.switcher.add_input(self.input)
    
    def _init_elements(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.content = PisakViewerContainer(self.context)
        self.add_child(self.content)
    

class PisakViewApp(object):
    """
    Main application class. This is the entry point .
    """
    def __init__(self, argv):
        """
        Initialize the aplication.
        @param argv application arguments
        """
        Clutter.init(argv)
        self._initialize_context()
        self._initialize_stage(argv)
    
    def _initialize_stage(self, argv):
        self.stage = PisakViewerStage(self.context)
        self.stage.connect("destroy", lambda _: Clutter.main_quit())
        self.stage.set_fullscreen(True)
        self.stage.show_all()
    
    def _initialize_context(self):
        self.context = switcher_app.Context(self)
    
    def main(self):
        """
        Starts the application main loop.
        """
        Clutter.main()


class SlideshowCycle(switcher_app.Cycle):
    def __init__(self, view_actor):
        self.view_actor = view_actor
        self.remaining = len(self.view_actor.photos)
    
    def has_next(self):
        return self.remaining > 0
    
    def expose_next(self):
        self.view_actor.next_photo()
    
    def select(self):
        raise NotImplementedError()


class PhotoViewIdleCycle(switcher_app.Cycle):
    def __init__(self, view_actor):
        self.view_actor = view_actor
    
    def has_next(self):
        return True
    
    def expose_next(self):
        pass
    
    def select(self):
        return self.view_actor.create_slideshow_cycle()


class PhotoView(Clutter.Actor):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self.photo_actor = Clutter.Actor()
        self.add_child(self.photo_actor)
        self.model = None
        self.photos = []
        self.current_photo = None

    def _update_photo(self, index):
        self.current_photo = index
        self.remove_child(self.photo_actor)
        self.photo_actor = Clutter.Actor()
        self.add_child(self.photo_actor)
    
    def set_model(self, model):
        self.model = model
        self._update_photo(self.model["initial_photo"])

    def create_slideshow_cycle(self):
        return SlideshowCycle(self)

    def create_idle_cycle(self):
        return PhotoViewIdleCycle(self)
    
    
    
    
    
    
