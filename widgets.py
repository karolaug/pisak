from gi.repository import Clutter, Mx, GObject
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



class TilePage(Clutter.Actor):
    def __init__(self, items, page):
        super().__init__()
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_row_spacing(unit.mm(12))
        self.layout.set_column_spacing(unit.mm(12))
        self.layout.set_column_homogeneous(True)
        self.layout.set_row_homogeneous(True)
        self.tiles = []
        for i in range(2):
            for j in range(3):
                index = int(page * 6 + i * 3 + j)
                if index < len(items):
                    tile = Tile()
                    tile.set_model(items[index])
                    self.tiles.append(tile)
                else:
                    tile = Clutter.Actor()
                self.layout.attach(tile, j, i, 1, 1)
    
    def start_cycle(self):
        self.cycle_active = True
        Clutter.threads_add_timeout(0, 1000, self.timeout_tile, None)
    
    def stop_cycle(self):
        self.cycle_active = False
    
    def timeout_tile(self, source):
        if self.cycle_active():  
            self.next_tile()
            return True
        else:
            return False
    
    def next_tile(self):
        self.next
        
    

class PagedTileView(Clutter.Actor):
    __gsignals__ = {
        "page-changed": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        "page-selected": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }

    def __init__(self):
        super(PagedTileView, self).__init__()
        self.page = None
        self.page_actor = None
        self.items = []
        self.page_interval = None
        self.cycle_active = False
        self.pages_current, self.pages_old = set(), set()
        self._init_tiles()
        self._paginate_items()
        self.start_cycle()
    
    def _init_tiles(self):
        self.layout = PagedViewLayout()
        self.set_layout_manager(self.layout)
    
    def generate_page(self, page):
        return TilePage(self.items, page)
    
    def timeout_page(self, source):
        if self.cycle_active:
            self.next_page()
            return True
        else:
            return False
    
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
            self.emit("page-changed", self.page)
        else:
            self.emit("page-changed", -1)
    
    def set_model(self, model):
        self.model = model
        self.items = self.model["items"]
        self.page_interval = self.model["page_interval"]
        self._paginate_items()
    
    def _paginate_items(self):
        self.page_count = int((len(self.items) + (6 - 1)) // 6)
        self.page = 0 if self.page_count else None
        self.update_page_actor()
        self.slide()
    
    def selection_tick(self):
        if self.selection.phase == "page":
            self.next_page()
        elif self.selection.phase == "row":
            self.next_row()
        else:
            self.next_column()
    
    def select(self):
        #if self.selection.phase == "page":
        self.emit("page-selected", self.page)
        #    #self.selection.phase = "row"
        #elif self.selection.phase == "row":
        #    self.selection.phase = "column"
        #else:
        #    self.emit("item-selected", 0)
    
    
    def start_cycle(self):
        self.cycle_active = True
        Clutter.threads_add_timeout(0, 3000, self.timeout_page, None)
    
    def stop_cycle(self):
        self.cycle_active = False
    
        

