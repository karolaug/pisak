"""
Module defines classes specific to Viewer application.
"""
import os.path
from gi.repository import Clutter, Mx, GObject
from pisak import unit, view
from pisak import widgets
from pisak import switcher_app
from pisak import res


class CategoryView(widgets.ScrollingView):
    """
    Actor widget which presents photos in the selected category.
    """
    MODEL = {
        "items": [{
              "label": "Zdjęcie %d" % i,
              "image_path": os.path.join(res.PATH, "krolikarnia.jpg")
            } for i in range(20)
        ],
        "page_interval": 6000
    }
    __gsignals__ = {
        "photo-selected": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }
    
    def __init__(self, context):
        super().__init__()
        self.context= context
        self.content_scroll.tile_handler = self.show_photo
    
    def _init_overlay(self):
        background_path = os.path.join(res.PATH, "hyperbolic_vignette.png")
        self.add_child(Clutter.Texture.new_from_file(background_path))

    def _tile_selected(self, scroll, photo):
        self.emit('photo-selected', photo)
    
    def show_photo(self, tile):
        print("show photo")

    
class LibraryView(widgets.ScrollingView):
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
    __gsignals__ = {
        "category-selected": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }
    
    def __init__(self, context):
        super().__init__()
        self.context= context
        self.content_scroll.tile_handler = self.show_category

    def _init_overlay(self):
        background_path = os.path.join(res.PATH, "hyperbolic_vignette.png")
        self.add_child(Clutter.Texture.new_from_file(background_path))

    def _tile_selected(self, scroll, category):
        self.emit('category-selected', category)

    def show_category(self, tile):
        self.context.application.push_view(CategoryView(self.context))


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
        self.button.set_label("Koniec")
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
        self.library_view = LibraryView(self.context)
        self.library_view.connect('category-selected', self.enter_category)
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

    def enter_category(self, library, category):
        self.category_view = CategoryView()
        self.category_view.connect('photo-selected', self.enter_photo)
        self.push_view(self.category_view)
        
    def enter_photo(self, category, photo):
        print('photo nr', photo, 'selected')
     
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
    
    def push_view(self, new_view):
        """
        Add new view to the container
        """
        self.main.push_view(new_view)
        self.context.switcher.push_cycle(new_view.create_cycle())


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
    
    def push_view(self, new_view):
        self.content.push_view(new_view)
    

class PisakViewApp(switcher_app.Application):
    """
    Pisak viewer app with pisak viewer stage.
    """    
    def create_stage(self, argv):
        stage = PisakViewerStage(self.context)
        stage.set_fullscreen(True)
        return stage


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
        self.photo_actor = widgets.PhotoSlide()
        self.photo_actor.set_model(self.photos[index])
        self.add_child(self.photo_actor)
    
    def set_model(self, model):
        self.model = model
        self.photos = self.model["items"]
        self.current_photo = self.model["initial_photo"]
        self._update_photo(self.current_photo)

    def create_slideshow_cycle(self):
        return SlideshowCycle(self)

    def create_idle_cycle(self):
        return PhotoViewIdleCycle(self)
    
    
    
    
    
    
