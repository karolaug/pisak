"""
Module defines classes specific to Viewer application.
"""
import os.path
import random
from gi.repository import Clutter, GObject
from pisak import unit, view
from pisak import widgets
from pisak import switcher_app
from pisak import res
from pisak.viewer import photo

class CategoryView(widgets.ScrollingView):
    """
    Actor widget which presents photos in the selected category.
    """
    MODEL = {
        "items": [{
              "label": "Zdjęcie %d" % i,
              "image_path": os.path.join(
                        res.PATH,
                        random.choice(["krolikarnia.jpg", "kolejka.jpg"]))
            } for i in range(20)
        ],
        "page_interval": 6000
    }
    __gsignals__ = {
        "photo-selected": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }
    
    def __init__(self, context):
        super().__init__(context)
        self.content_scroll.tile_handler = self.show_photo

    def _tile_selected(self, scroll, photo):
        self.emit('photo-selected', photo)
    
    def show_photo(self, tile):
        self.context.application.push_view(photo.PhotoView(self.context))

    
class LibraryView(widgets.ScrollingView):
    """
    Actor widget which presents categories in the photo library.
    """
    MODEL = {
        "items": [{
              "label": "Kategoria %d" % i,
              "image_path": os.path.join(
                        res.PATH,
                        random.choice(["krolikarnia.jpg", "kolejka.jpg"]))
            } for i in range(20)
        ],
        "page_interval": 6000
    }
    __gsignals__ = {
        "category-selected": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }
    
    def __init__(self, context):
        super().__init__(context)
        self.content_scroll.tile_handler = self.show_category

    def _tile_selected(self, scroll, category):
        self.emit('category-selected', category)

    def show_category(self, tile):
        self.context.application.push_view(CategoryView(self.context))


class PisakViewerContainer(view.BasicViewContainer):
    def __init__(self, context):
        """
        Application container, which creates other widgets.
        @param contect switcher application context passed from application
        """
        super().__init__(context)
        self._init_elements()
        
    def _init_main(self):
        #elf.library_view = LibraryView(self.context)
        #elf.library_view.connect('category-selected', self.enter_category)
        #elf.main = view.BasicViewContainer(self.context)
        #self.main.push_view(self.library_view)
        self.set_x_expand(True)
        self.set_y_expand(True)

    def _init_elements(self):
        self._init_main()
        #self.buttons = PisakViewerButtons(self)
        
        #self.buttons.set_y_expand(True)
        #self.buttons.set_x_expand(False)
        #self.buttons.set_width(unit.mm(25))
        #self.buttons.set_depth(-1.0)
        
        layout = Clutter.BoxLayout()
        layout.set_orientation(Clutter.Orientation.HORIZONTAL)
        self.set_layout_manager(layout)
        layout.set_spacing(unit.mm(4))
        #self.add_child(self.main)
        #self.add_child(self.buttons)

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
    
    #def create_cycle(self):
        #"""
        #Create new page-switching cycle in the library view
        #"""
        #return self.library_view.create_cycle()
    
    #def push_view(self, new_view):
        #"""
        #Add new view to the container
        #"""
        #self.main.push_view(new_view)
        #self.context.switcher.push_cycle(new_view.create_cycle())


class PisakViewerStage(Clutter.Stage):
    def __init__(self, context):
        """
        Clutter stage which sets up the switcher application.
        @param context switcher application context passed from application
        """
        super(PisakViewerStage, self).__init__()
        self.context = context
        self._init_elements()
        #self.context.switcher.push_cycle(self.content.create_cycle())
        self._init_input()

    def _init_elements(self):
        self._init_layout()
        self._init_background()
        self._init_content()
    
    def _init_content(self):
        self.content = PisakViewerContainer(self.context)
        self.add_child(self.content)
        library_view = LibraryView(self.context)
        self.content.push_view(library_view)

    def _init_background(self):
        def fence_pattern(canvas, context, w, h):
            context.scale(w, h)
            context.set_line_width(0.05)
            context.set_source_rgba(0, 0, 0, 0.15)
            lines = [(0, 0, 1, 1), (0, 1, 1, 0)]
            for x1, y1, x2, y2 in lines:
                context.move_to(x1, y1)
                context.line_to(x2, y2)
                context.stroke()
            return True
        background_image = Clutter.Canvas()
        background_image.set_size(unit.mm(2), unit.mm(2))
        background_image.connect("draw", fence_pattern)
        background_image.invalidate()
        self.set_content(background_image)
        self.set_content_repeat(Clutter.ContentRepeat.BOTH)
        self.set_content_scaling_filters(Clutter.ScalingFilter.TRILINEAR, Clutter.ScalingFilter.TRILINEAR)
    
    def push_view(self, new_view):
        self.content.push_view(new_view)

    def _init_input(self):
        self.input = switcher_app.KeyboardSwitcherInput(self)
        self.context.switcher.add_input(self.input)

    def _init_layout(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)


class PisakViewApp(switcher_app.Application):
    """
    Pisak viewer app with pisak viewer stage.
    """    
    def create_stage(self, argv):
        stage = PisakViewerStage(self.context)
        stage.set_fullscreen(True)
        return stage
