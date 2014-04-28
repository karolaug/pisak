'''
Viewing and operations on photos (images with metadata)
'''
from pisak import buttons, unit, widgets, res, switcher_app
from gi.repository import Clutter, Mx
import os.path

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
    interval = 3600
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
        self.set_layout_manager(Clutter.BoxLayout())
        self.set_x_expand(True)
        self.set_y_expand(True)
        self.photo_actor = Mx.Image()
        self.photo_actor.set_from_file(os.path.join(res.PATH, "krolikarnia.jpg"))
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
    
    def create_cycle(self):
        return self.create_idle_cycle()
    

class PhotoEditionMenu(Clutter.Actor):
    """
    Widget of buttons associated with a PhotoView being in the edition mode.
    @param view an instance of PhotoView.
    """
    SPACING = unit.mm(4)
    def __init__(self, view):
        super().__init__()
        self.view = view
        self.buffer = view.buffer
        self._init_layout()
        self._init_buttons()
        
    def _init_layout(self):
        self.layout = Clutter.BoxLayout()
        self.layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.layout.set_spacing(self.SPACING)
        self.set_layout_manager(self.layout)
        margin = Clutter.Margin()
        margin.top = margin.bottom = self.SPACING
        self.set_margin(margin)

    def _init_buttons(self):
        self.buttons = {'grayscale': ['skala szarości', self.buffer.grayscale], 'save': ['zapisz', self.buffer.save],
                        'original': ['oryginał', self.buffer.original], 'mirror': ['lustro', self.buffer.mirror],
                        'rotate': ['obróć', self.buffer.rotate], 'zoom': ['powiększenie', self.buffer.zoom],
                        'invert': ['negatyw', self.buffer.invert], 'edges': ['krawędzie', self.buffer.edges],
                        'contour': ['szkic', self.buffer.contour], 'noise': ['szum', self.buffer.noise],
                        'sepia': ['sepia', self.buffer.sepia], 'solarize': ['prześwietlenie', self.buffer.solarize]}
        for b in self.buttons:
            button = buttons.MenuButton()
            button.set_model({'label': self.buttons[b][0]})
            button.connect('activate', self.buttons[b][1])
            self.add_child(button) 
