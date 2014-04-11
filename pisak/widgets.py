from gi.repository import Clutter, Mx, GObject
from pisak import unit, switcher_app
import collections

class Tile(Clutter.Actor):
    __gsignals__ = {
        "activate": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        super(Tile, self).__init__()
        self._init_elements()
        self.hilite = 0.0

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

    def hilite_off(self):
        self.set_hilite(0.0)
    
    def hilite_on(self):
        self.set_hilite(1.0)
    
    def set_hilite(self, hilite):
        self.hilite = hilite
        if self.hilite < 0.5:
            color = Clutter.Color.new(255, 255, 255, 0)
        else:
            color = Clutter.Color.new(64, 128, 192, 192)
        self.set_background_color(color)


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


class _TilePageCycle(switcher_app.Cycle):
    def __init__(self, actor):
        self.actor = actor
        self.index = None
        self.interval = 1000
        self.remaining = len(self.actor.tiles) * 2
    
    def expose_next(self):
        if self.index != None:
            self.actor.tiles[self.index].hilite_off()
            self.index = (self.index + 1) % len(self.actor.tiles)
        else:
            self.index = 0
        self.actor.tiles[self.index].hilite_on()
        self.remaining -= 1
    
    def has_next(self):
        return self.remaining > 0
    
    def stop(self):
        if self.index != None:
            self.actor.tiles[self.index].hilite_off()
            self.index = None
    
    def select(self):
        activated_actor = self.actor.tiles[self.index]
        return switcher_app.selection_activate_actor(activated_actor)


class TilePage(Clutter.Actor):
    __gsignals__ = {
        "tile-selected": (GObject.SIGNAL_RUN_FIRST, None, (int,))
    }
    
    def __init__(self, tiles):
        """
        Create a page of tiles aligned in grid.
        @param tiles A list of tiles to be placed on the page.
        """
        super().__init__()
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_row_spacing(unit.mm(12))
        self.layout.set_column_spacing(unit.mm(12))
        self.layout.set_column_homogeneous(True)
        self.layout.set_row_homogeneous(True)
        self.tiles = tiles
        for i in range(2):
            for j in range(3):
                index = int(i * 3 + j)
                tile = tiles[index] if index < len(tiles) else Clutter.Actor()
                self.layout.attach(tile, j, i, 1, 1)

    def select(self, tile):
        self.emit("tile-selected", tile)
    
    def create_cycle(self):
        return _TilePageCycle(self)

class _PagedTileViewCycle(switcher_app.Cycle):
    def __init__(self, actor):
        self.actor = actor
        self.interval = 3000
    
    def expose_next(self):
        self.actor.next_page()
    
    def has_next(self):
        return True
    
    def stop(self):
        pass
    
    def select(self):
        cycle =  self.actor.page_actor.create_cycle()
        return switcher_app.selection_add_cycle(cycle)

class PagedTileView(Clutter.Actor):
    __gsignals__ = {
        "page-changed": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        "tile-selected": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    }

    def __init__(self):
        super(PagedTileView, self).__init__()
        self.page = None
        self.page_actor = None
        self.items = []
        self.page_interval = None
        self.pages_current, self.pages_old = set(), set()
        self.tile_handler = None
        self._init_tiles()
        self._paginate_items()
    
    @property
    def tile_handler(self):
        return self._tile_handler
    
    @tile_handler.setter
    def tile_handler(self, value):
        if value == None or isinstance(value, collections.Callable):
            self._tile_handler = value
        else:
            raise ValueError("Handler is not callable")
    
    def _init_tiles(self):
        self.layout = PagedViewLayout()
        self.set_layout_manager(self.layout)
    
    def generate_page(self, page):
        tiles = []
        
        for i in range(6):
            index = int(page * 6 + i)
            if index < len(self.items):
                tile = Tile()
                tile.connect("activate", self.activate_tile)
                tile.set_model(self.items[index])
                tiles.append(tile)
        return TilePage(tiles)
    
    def activate_tile(self, source):
        if self.tile_handler:
            self.tile_handler(source)
    
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
            self.page_actor.connect("tile-selected", self._tile_selected)
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
    
    def _tile_selected(self, page, tile):
        self.emit("tile-selected", tile)
    
    def create_cycle(self):
        return _PagedTileViewCycle(self)


class ScrollingView(Clutter.Actor):
    """
    Base class for widgets presenting scrolling paged tiles.
    """
    def __init__(self):
        super().__init__()
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
        self.content_scrollbar = ProgressBar()
        self.content_scrollbar.set_x_expand(True)
        self.content_scrollbar.set_height(30)
        self.content.add_child(self.content_scrollbar)
    
    def _init_content_scroll(self):
        self.content_scroll = PagedTileView()
        self.content_scroll.set_model(self.MODEL)
        self.content_scroll.connect("page-changed", self._update_scrollbar)
        self.content_scroll.connect("tile-selected", self._tile_selected)
        self.content.add_child(self.content_scroll)
        
    def _init_content_layout(self):
        self.content_layout = Clutter.BoxLayout()
        self.content.set_layout_manager(self.content_layout)
        self.content_layout.set_orientation(Clutter.Orientation.VERTICAL)
        #self.content_layout.set_spacing(30)
    
    def _init_overlay(self):
        raise NotImplementedError()
    
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

    def _tile_selected(self, scroll, tile):
        raise NotImplementedError()
    
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


class ProgressBar(Clutter.Actor):
    __gproperties__ = {
        'progress': (GObject.TYPE_FLOAT, None, None, 0, 1, 0, GObject.PARAM_READWRITE)
    }
    
    def __init__(self):
        super(ProgressBar, self).__init__()
        self.progress = 0
        self.canvas = None
        self.connect("notify::progress", self.update_bar)

    def do_set_property(self, prop, value):
        self.progress = value
        
    def do_get_property(self, prop):
        return self.progress
        
    def update_bar(self, bar, prop):
        def update_canvas(canvas, context, width, height):
            context.scale(width, height)
            context.rectangle(0, 0, self.progress, 1)
            context.set_source_rgba(0, 0.5, 0.5, 1)
            context.fill()
            context.rectangle(self.progress, 0, 1, 1)
            context.set_source_rgba(0, 0, 0, 1)
            context.fill()
            return True
        if self.canvas:
            self.canvas.invalidate()
        else:
            self.canvas = Clutter.Canvas()
            self.canvas.set_size(unit.mm(20), unit.mm(5))
            self.canvas.connect("draw", update_canvas)
            self.set_content(self.canvas)
            self.canvas.invalidate()
        
        
class PhotoSlide(Clutter.Actor):
    def __init__(self):
        super().__init__()
        self.image_actor = Mx.Image()
        self.add_child(self.image_actor)
    
    def set_model(self, model):
        self.model = model
        self.image_actor.set_from_file(self.model["photo_path"])

