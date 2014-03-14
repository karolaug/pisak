from gi.repository import Clutter, Mx
import unit
import time

class Tile(Clutter.Actor):
    def __init__(self):
        super(Tile, self).__init__()
        self._init_elements()
        
    def _init_elements(self):
        self._init_preview()
        self._init_label()
        self._init_layout()
    
    def _init_preview(self):
        self.preview = Mx.Image()
        self.add_child(self.preview)
        self.preview.set_scale_mode(Mx.ImageScaleMode.FIT)
    
    def _init_label(self):
        self.label = Mx.Label()
        self.add_child(self.label)
    
    def _init_layout(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_orientation(Clutter.Orientation.VERTICAL)
    
    def set_label(self, text):
        self.label.set_text(text)
    
    def set_preview_from_file(self, path):
        self.preview.set_from_file(path)
    
    def set_model(self, model):
        self.set_label(model["label"])
        if "image_path" in model:
            self.set_preview_from_file(model["image_path"])


class PagedViewLayout(Clutter.BinLayout):
    def __init__(self):
        super(PagedViewLayout, self).__init__()
        self.pages_new = set()
        self.pages_old = set()
    
    def do_allocate(self, container, allocation, flags):
        for child in container.get_children():
            if child in self.pages_new:
                child.set_easing_duration(0)
                allocation.set_origin(allocation.get_width(), 0)
                child.allocate(allocation, flags)
                child.set_easing_duration(600)
                allocation.set_origin(0, 0)
                child.allocate(allocation, flags)
            elif child in self.pages_old:
                allocation.set_origin(-allocation.get_width(), 0)
                child.allocate(allocation, flags)
    def slide(self, new, old):
        self.pages_new, self.pages_old = new, old
        self.layout_changed()


class PagedTileView(Clutter.Actor):
    def __init__(self):
        super(PagedTileView, self).__init__()
        self.page = None
        self.page_actor = None
        self.items = []
        self.pages_current, self.pages_old = set(), set()
        self._init_tiles()
        self._paginate_items()
    
    def _init_tiles(self):
        self.layout = PagedViewLayout()
        self.set_layout_manager(self.layout)
    
    def generate_page(self, page):
        page_actor = Clutter.Actor()
        page_layout = Clutter.GridLayout()
        page_actor.set_layout_manager(page_layout)
        page_layout.set_row_spacing(unit.mm(12))
        page_layout.set_column_spacing(unit.mm(12))
        page_layout.set_column_homogeneous(True)
        page_layout.set_row_homogeneous(True)
        for i in range(2):
            for j in range(3):
                index = int(page * 6 + i * 3 + j)
                if index < len(self.items):
                    tile = Tile()
                    tile.set_model(self.items[index])
                else:
                    tile = Clutter.Actor()
                page_layout.attach(tile, j, i, 1, 1)
        return page_actor
    
    def next_page(self):
        if self.page == None:
            self.page = 0
        else:
            self.page = (self.page + 1) % self.page_count
        self.update_page_actor()
        self.slide()
    
    def slide(self):
        # remove old
        for page in self.pages_old:
            self.remove_child(page)
            page.destroy()
        # mark current as old
        self.pages_old = self.pages_current
        # mark unmarked as current
        self.pages_current = set(self.get_children()) - self.pages_current
        self.layout.slide(self.pages_current, self.pages_old)
    
    def update_page_actor(self):
        if self.page != None:
            self.page_actor = self.generate_page(self.page)
            self.add_child(self.page_actor)
    
    def set_model(self, model):
        self.model = model
        self.items = self.model["items"]
        self._paginate_items()
    
    def _paginate_items(self):
        self.page_count = int((len(self.items) + (6 - 1)) // 6)
        self.page = 0 if self.page_count else None
        self.update_page_actor()
        self.slide()

