from gi.repository import Clutter, Mx, GObject, Rsvg, Cogl
import os.path
from pisak import switcher_app, unit, res
from pisak.layout import Box
import collections
from pisak.res import colors, dims
import cairo

class PropertyAdapter(object):

    def find_attribute(self, name):
        name  = self._repair_prop_name(name)
        for relative in self.__class__.mro():
            attribute = relative.__dict__.get(name)
            if attribute:
                break
        return attribute

    @staticmethod
    def _repair_prop_name(name):
        if '-' in name:
            name = name.replace('-', '_')
        return name

    def do_set_property(self, spec, value):
        """
        Introspect object properties and set the value.
        """
        attribute = self.find_attribute(spec.name)
        if attribute is not None and isinstance(attribute, property):
            attribute.fset(self, value)
        else:
            raise ValueError("No such property", spec.name)

    def do_get_property(self, spec):
        """
        Introspect object properties and get the value.
        """
        attribute = self.find_attribute(spec.name)
        if attribute is not None and isinstance(attribute, property):
            return attribute.fget(self)
        else:
            raise ValueError("No such property", spec.name)

class Header(Mx.Image, PropertyAdapter):

    __gtype_name__ = "PisakMenuHeader"

    __gproperties__ = {
        "name": (GObject.TYPE_STRING, None, None, "funkcjenapis", 
                 GObject.PARAM_READWRITE)}

    def __init__(self):
        super().__init__()
        self.handle = Rsvg.Handle()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        svg_path = os.path.join(res.PATH, 'icons', 
                                ''.join([self.name, ".svg"]))
        self.svg = self.handle.new_from_file(svg_path)
        pixbuf = self.svg.get_pixbuf()
        self.set_from_data(pixbuf.get_pixels(),
                           Cogl.PixelFormat.RGBA_8888, 
                           pixbuf.get_width(), 
                           pixbuf.get_height(), 
                           pixbuf.get_rowstride())

class Button(Mx.Button, PropertyAdapter):
    """
    Generic Pisak button widget with label and icon.
    """
    __gsignals__ = {
        "activate": (GObject.SIGNAL_RUN_FIRST, None, ()),
        "inactivate": (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    
    __gproperties__ = {
        "ratio_width": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_height": (
            GObject.TYPE_FLOAT, None, None, 0,
            1., 0, GObject.PARAM_READWRITE),
        "text": (
            GObject.TYPE_STRING, "label default text",
            "text displayed on the button", "noop",
            GObject.PARAM_READWRITE),
        "alternative_text": (
            GObject.TYPE_STRING,
            "alternative label text",
            "alternative text displayed on the button",
            "?", GObject.PARAM_READWRITE),
        "icon_name": (
            GObject.TYPE_STRING, "blank",
            "name of the icon displayed on the button",
            "blank", GObject.PARAM_READWRITE),
        "alternative_icon_name":(
            GObject.TYPE_STRING, "blank",
            "name of the aternative icon displayed on the button",
            "blank", GObject.PARAM_READWRITE),
        "spacing": (
            GObject.TYPE_INT64, "space between icon and text",
            "space between icon and text", 0, 1000, 100, 
            GObject.PARAM_READWRITE)
    }
    
    def __init__(self):
        super().__init__()
        self.properties = {}
        self.selection_time = 1000
        self.current_icon = None
        self._connect_signals()

    def _connect_signals(self):
        self.connect("notify::text", self._set_initial_label)
        self.connect("clicked", self.click_activate)
        #self.connect("enter-event", lambda *_: self.hilite_on())
        #self.connect("leave-event", lambda *_: self.hilite_off())
        self.connect("inactivate", lambda *_: self.inactivate())
        self.connect("notify::style-pseudo-class", 
                     lambda *_: self.change_icon_white())
        self.set_reactive(True)

    @property
    def ratio_width(self):
        return self._ratio_width

    @ratio_width.setter
    def ratio_width(self, value):
        self._ratio_width = value
        self.set_width(unit.w(value))

    @property
    def ratio_height(self):
        return self._ratio_height

    @ratio_height.setter
    def ratio_height(self, value):
        self._ratio_height = value
        self.set_height(unit.h(value))

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = str(value)

    @property
    def alternative_text(self):
        return self._alternative_text

    @alternative_text.setter
    def alternative_text(self, value):
        self._alternative_text = str(value)
    
    @property
    def icon_name(self):
        return self._icon_name
    
    @icon_name.setter
    def icon_name(self, value):
        self._icon_name = value
        if not Mx.IconTheme.get_default().has_icon(value):
            self.set_icon()

    @property
    def alternative_icon_name(self):
        return self._alternative_icon_name
    
    @alternative_icon_name.setter
    def alternative_icon_name(self, value):
        self._alternative_icon_name = value

    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, value):
        self._spacing = value
        #self.box.set_spacing(value)

    def _set_initial_label(self, source, spec):
        self.set_default_label()
        self.disconnect_by_func(self._set_initial_label)

    def set_default_label(self):
        self.set_label(self.text)

    def set_alternative_label(self):
        self.set_label(self.alternative_text)

    def switch_label(self):
        current_label = self.get_label()
        if current_label in (self.alternative_text, None):
            self.set_default_label()
        elif current_label == self.text:
            self.set_alternative_label()

    def switch_icon(self):
        raise NotImplementedError

    def set_icon(self):
        if self.icon_name:
            self.custom_content()
            self.read_svg()
            self.set_image()

            text_length = len(self.get_label())
            if text_length == 1:
                pass
            else:
                pass
            #self.space.set_width(self.get_width() - 200 - self.image.get_width())
            self.box.show()
            if self.image not in self.box.get_children():
                self.box.add_child(self.space)
                self.box.add_child(self.image)
        else:
            try:
                self.box.hide()
            except AttributeError:
                return None

    def custom_content(self):
        self.set_icon_visible(False)
        self.space = Clutter.Actor()
        if not hasattr(self, "box"):
            self.box = Box()
            self.get_children()[0].add_actor(self.box, 1)

    def read_svg(self):
        try:
            handle = Rsvg.Handle()
            svg_path = ''.join([os.path.join(res.PATH,'icons',
                                             self.icon_name), '.svg'])
            self.svg = handle.new_from_file(svg_path)
        except: #GError as error:
            print('No file found at {}.'.format(svg_path))
            self.svg = False

    def set_image(self):
        if not hasattr(self, "image"):
            self.image = Mx.Image()
        self.image_path = os.path.join(res.PATH, "icons", self.icon_name)
        icon_size = self.get_icon_size()
        if self.svg:
            pixbuf = self.svg.get_pixbuf()
            if icon_size:
                pixbuf = pixbuf.scale_simple(icon_size, icon_size, 3)
            self.image.set_from_data(pixbuf.get_pixels(),
                                     Cogl.PixelFormat.RGBA_8888, 
                                     pixbuf.get_width(), 
                                     pixbuf.get_height(), 
                                     pixbuf.get_rowstride())
        else:
            try:
                self.image.set_from_file(''.join([self.image_path, '.png']))
            except: # GError as error:
                print("No PNG, trying JPG")
                try:
                    self.image.set_from_file(''.join([self.image_path, 
                                                      '.jpg']))
                except: # GError as error:
                    text = "No PNG, SVG or JPG icon found of name {}." 
                    print(text.format(self.icon_name))
            self.image.set_scale_mode(1) #1 is FIT, 0 is None, 2 is CROP
            if icon_size:
                image_size = self.image.get_size()
                print(image_size, icon_size)
                self.image.set_scale(icon_size * 10 / image_size[1],
                                     icon_size * 10/ image_size[0])

    def set_image_white(self):
        handle = Rsvg.Handle()
        svg_path = ''.join([os.path.join(res.PATH,'icons',
                                         self.icon_name), '_white', '.svg'])
        self.svg_white = handle.new_from_file(svg_path)
        icon_size = self.get_icon_size()
        pixbuf = self.svg_white.get_pixbuf()
        if icon_size:
            pixbuf = pixbuf.scale_simple(icon_size, icon_size, 3)
        self.image.set_from_data(pixbuf.get_pixels(),
                                 Cogl.PixelFormat.RGBA_8888, 
                                 pixbuf.get_width(), 
                                 pixbuf.get_height(), 
                                 pixbuf.get_rowstride())


    def change_icon_white(self):
        try:
            if self.icon_name:
                if self.style_pseudo_class_contains("hover"):
                    self.set_image_white()
                else:
                    pixbuf = self.svg.get_pixbuf()
                    icon_size = self.get_icon_size()
                    if icon_size:
                        pixbuf = pixbuf.scale_simple(icon_size, icon_size, 3)
                        self.image.set_from_data(pixbuf.get_pixels(),
                                                 Cogl.PixelFormat.RGBA_8888, 
                                                 pixbuf.get_width(), 
                                                 pixbuf.get_height(), 
                                                 pixbuf.get_rowstride())
        except AttributeError:
            pass
            
    def hilite_off(self):
        self.style_pseudo_class_remove("hover")
    
    def hilite_on(self):
        self.style_pseudo_class_add("hover")

    def select_on(self):
        self.style_pseudo_class_add("active")

    def inactivate(self):
        self.style_pseudo_class_remove("active")
    
    def click_activate(self, source):
        self.select_on()
        Clutter.threads_add_timeout(0, self.selection_time, lambda _: self.hilite_off(), None)
        self.emit("activate")


class BackgroundPattern(Clutter.Actor):
    __gtype_name__ = "PisakBackgroundPattern"

    def __init__(self):
        super().__init__()
        background_image = Clutter.Canvas()
        background_image.set_size(unit.mm(2), unit.mm(2))
        background_image.connect("draw", self.fence_pattern)
        background_image.invalidate()
        self.set_content(background_image)
        self.set_content_repeat(Clutter.ContentRepeat.BOTH)
        self.set_content_scaling_filters(Clutter.ScalingFilter.TRILINEAR, Clutter.ScalingFilter.TRILINEAR)

    @staticmethod
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


class Aperture(Clutter.Actor):
    __gproperties__ = {
        'cover': (GObject.TYPE_FLOAT, None, None, 0, 1, 0, GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.set_x_expand(True)
        self.set_y_expand(True)
        self.properties = {}
        self.color = colors.HILITE_1
        self._init_content()
        self.connect("notify::cover", self._update_cover)
        self.set_property("cover", 0)

    def _update_cover(self, source, prop):
        self.canvas.invalidate()

    def set_cover(self, value):
        self.remove_transition("cover")
        transition = Clutter.PropertyTransition.new("cover")
        transition.set_from(self.properties["cover"])
        transition.set_to(value)
        transition.set_duration(166)
        self.add_transition("cover", transition)

    def do_set_property(self, p, value):
        self.properties[p.name] = value

    def do_get_property(self, p):
        if p.name in self.properties:
            return self.properties[p.name]
        else:
            raise AttributeError("Unknown property", p.name)

    def draw(self, canvas, context, w, h):
        #context.scale(w / 2, h)
        context.set_operator(cairo.OPERATOR_CLEAR)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)
        context.rectangle(0, 0, w, h)
        context.set_source_rgba(0, 0.894, 0.765, 0.66)
        context.fill()
        context.set_operator(cairo.OPERATOR_CLEAR)
        a = 1 - (self.properties["cover"])
        x, y = (0.5 - a / 2) * w, (0.5 - a / 2) * h
        rw, rh = a * w, a * h
        context.rectangle(x, y, rw, rh)
        context.fill()
        return True

    def _init_content(self):
        self.canvas = Clutter.Canvas()
        self.canvas.set_size(140, 140)
        self.canvas.connect("draw", self.draw)
        self.set_content(self.canvas)


class Tile(Clutter.Actor):
    __gsignals__ = {
        "activate": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        super(Tile, self).__init__()
        self.set_size(dims.TILE_W_PX, dims.TILE_H_PX)
        self._init_elements()
        self.hilite = 0.0

    def _init_aperture(self):
        self.aperture = Aperture()
        self.add_child(self.aperture)

    def _init_elements(self):
        self._init_preview()
        self._init_label()
        self._init_aperture()
        self._init_layout()

    def _init_preview(self):
        self.preview = Mx.Image()
        self.add_child(self.preview)
        #TODO: upscaling
        self.preview.set_scale_mode(Mx.ImageScaleMode.CROP)

    def _init_label(self):
        self.label = Mx.Label()
        self.add_child(self.label)

    def _init_layout(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

    def set_label(self, text):
        self.label.set_text(text)

    def set_preview_from_file(self, path):
        self.preview.set_from_file(path)

    def set_model(self, model):
        self.set_label(model["label"])
        if "image_path" in model:
            self.set_preview_from_file(model["image_path"])

    def hilite_off(self):
        self.aperture.set_cover(0)
        self.set_hilite(0.0)

    def hilite_on(self):
        self.aperture.set_cover(0.5)
        self.set_hilite(1.0)

    def set_hilite(self, hilite):
        self.hilite = hilite
        if self.hilite < 0.5:
            color = colors.TRANSPARENT
        else:
            color = colors.HILITE_1
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
        self.remaining = len(self.actor.tiles)

    def expose_next(self):
        if self.index is not None:
            self.actor.tiles[self.index].hilite_off()
            self.index = (self.index + 1) % len(self.actor.tiles)
        else:
            self.index = 0
        self.actor.tiles[self.index].hilite_on()
        self.remaining -= 1

    def has_next(self):
        return self.remaining > 0

    def stop(self):
        if self.index is not None:
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
        self.set_width(3 * dims.TILE_W_PX + 2 * dims.W_SPACING_PX)
        self.set_height(4 * dims.TILE_H_PX + 3 * dims.H_SPACING_PX)
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self.layout.set_row_spacing(dims.H_SPACING_PX)
        self.layout.set_column_spacing(dims.W_SPACING_PX)
        self.tiles = tiles
        for i in range(4):
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
        cycle = self.actor.page_actor.create_cycle()
        return switcher_app.selection_add_cycle(cycle)


class PagedTileView(Clutter.Actor):
    __gsignals__ = {
        "page-changed": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
        "tile-selected": (GObject.SIGNAL_RUN_FIRST, None, (int,)),
    }

    def __init__(self):
        super(PagedTileView, self).__init__()
        self.set_clip_to_allocation(True)
        self.page = None
        self.page_actor = None
        self.items = []
        self.page_interval = None
        self.pages_current = set()
        self.pages_old = set()
        self.tile_handler = None
        self._init_tiles()
        self._paginate_items()

    @property
    def tile_handler(self):
        return self._tile_handler

    @tile_handler.setter
    def tile_handler(self, value):
        if value is None or isinstance(value, collections.Callable):
            self._tile_handler = value
        else:
            raise ValueError("Handler is not callable")

    def _init_tiles(self):
        self.layout = PagedViewLayout()
        self.set_layout_manager(self.layout)

    def generate_page(self, page):
        tiles = []

        for i in range(12):
            index = int(page * 12 + i)
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
        if self.page is None:
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
        if self.page is not None:
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
        self.page_count = int((len(self.items) + (12 - 1)) // 12)
        self.page = 0 if self.page_count else None
        self.update_page_actor()
        self.slide()

    def _tile_selected(self, page, tile):
        self.emit("tile-selected", tile)

    def create_cycle(self):
        return _PagedTileViewCycle(self)


class ScrollingViewCycle(switcher_app.Cycle):
    interval = 1000

    def __init__(self, actor):
        super().__init__()
        self.actor = actor
        self.index = 0

    def expose_next(self):
        self.STEPS[self.index](self)
        self.index = (self.index + 1) % len(self.STEPS)

    def stop(self):
        self.actor.menu.hilite_off()

    def has_next(self):
        return True

    def show_menu(self):
        self.actor.menu.hilite_on()

    def show_page(self):
        self.actor.select_page()

    def next_page(self):
        pass
        self.actor.next_page()


ScrollingViewCycle.STEPS = [
    ScrollingViewCycle.show_menu, ScrollingViewCycle.show_page,
    ScrollingViewCycle.next_page]


class SideMenu(Clutter.Actor):
    """
    Display vertical menu on the side of a view. Abstract class,
    generates buttons from BUTTONS class variable.

    deprecated::
    """

    def __init__(self, context):
        """
        Create menu

        :param context: Switcher application context
        """
        super().__init__()
        self.context = context
        
        self._init_layout()
        self._init_buttons()

    def _init_buttons(self):
        menu_model = self.__class__.BUTTONS
        for button_model in menu_model:
            button = Button()
            #button.set_model(button_model)
            self.add_child(button)

    def _init_layout(self):
        # set up layout manager
        self.layout = Clutter.BoxLayout()
        self.layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.layout.set_spacing(dims.H_SPACING_PX)
        self.set_layout_manager(self.layout)
        # set dimensions
        self.set_y_expand(True)
        self.set_width(dims.MENU_BUTTON_W_PX)

    def hilite_off(self):
        self.set_hilite(0.0)

    def hilite_on(self):
        self.set_hilite(1.0)

    def set_hilite(self, hilite):
        self.hilite = hilite
        if self.hilite < 0.5:
            color = colors.TRANSPARENT
        else:
            color = colors.HILITE_1
        self.set_background_color(color)


class LibraryViewMenu(SideMenu):
    BUTTONS = [
        {
            "label": "Whatevs",
            "icon": None,
            "handler": None},
        {
            "label": "Wyjście",
            "icon": None,
            "handler": None}]


class CategoryViewMenu(SideMenu):
    BUTTONS = [
        {
            "label": "Whatevs",
            "icon": None,
            "handler": None},
        {
            "label": "Powrót",
            "icon": None,
            "handler": None},
        {
            "label": "Wyjście",
            "icon": None,
            "handler": None}]


class ScrollingView(Clutter.Actor):
    """
    Base class for widgets presenting scrolling paged tiles.
    """
    def __init__(self, context):
        super().__init__()
        self.context = context
        self._init_elements()

    def _init_elements(self):
        self._init_layout()
        self._init_content()

    def _init_layout(self):
        margin = Clutter.Margin()
        margin.top = margin.bottom = dims.H_SPACING_PX
        self.set_margin(margin)
        self.layout = Clutter.GridLayout()
        self.layout.set_row_spacing(dims.H_SPACING_PX)
        self.layout.set_column_spacing(dims.W_SPACING_PX)
        self.set_layout_manager(self.layout)

    def _init_content(self):
        self._init_menu()
        self._init_content_header()
        self._init_content_scrollbar()
        self._init_content_scroll()

    def create_menu(self):
        '''
        Abstract method which should create and return a menu actor.
        '''
        raise NotImplementedError("Menu creation not implemented")
    
    def _init_menu(self):
        self.menu = self.create_menu()
        self.menu.set_y_expand(False)
        self.layout.attach(self.menu, 0, 0, 1, 2)

    def _init_content_header(self):
        self.header = Mx.Label()
        self.header.set_text("HELLO")
        self.header.set_height(dims.MENU_BUTTON_H_PX)
        self.header.set_x_expand(True)
        self.header.set_background_color(colors.HILITE_1)
        self.layout.attach(self.header, 1, 0, 1, 1)

    def _init_content_scrollbar(self):
        self.content_scrollbar = SignedProgressBar()
        self.content_scrollbar.set_height(dims.MENU_BUTTON_H_PX)
        self.content_scrollbar.set_x_expand(True)
        self.layout.attach(self.content_scrollbar, 0, 2, 2, 1)

    def _init_content_scroll(self):
        self.content_scroll = PagedTileView()
        self.content_scroll.connect("page-changed", self._update_scrollbar)
        self.content_scroll.set_model(self.MODEL)
        self.layout.attach(self.content_scroll, 1, 1, 1, 1)

    def _init_content_layout(self):
        self.content_layout = Clutter.BoxLayout()
        self.content_layout.set_spacing(dims.H_SPACING_PX)
        self.content.set_layout_manager(self.content_layout)
        self.content_layout.set_orientation(Clutter.Orientation.VERTICAL)

    def next_page(self):
        """
        Force next page in view.
        """
        self.content_scroll.next_page()

    def select_page(self):
        """
        Push cycle of the current page
        """
        page_actor = self.content_scroll.page_actor
        page_cycle = page_actor.create_cycle()
        self.context.switcher.push_cycle(page_cycle)

    def _update_scrollbar(self, scroll, page):
        if page == -1:
            progress = 0.0
        elif scroll.page_count == 1:
            progress = 1.0
        else:
            progress = page / (scroll.page_count - 1.0)
        self.content_scrollbar.update(progress, page, scroll.page_count)

    def create_initial_cycle(self):
        """
        Create a new cycle which is used by switcher to show consecutive pages from the model.
        """
        return ScrollingViewCycle(self)


class ProgressBar(Clutter.Actor):
    __gproperties__ = {
        'progress': (GObject.TYPE_FLOAT, None, None, 0, 1, 0, GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super(ProgressBar, self).__init__()
        self._init_bar()
        self._init_transition()
        self.connect("notify::progress", lambda source, prop: self.canvas.invalidate())
        self.set_property('progress', 0)
        self.connect("allocation-changed", lambda *_: self._resize_canvas())

    def _resize_canvas(self):
        self.canvas.set_size(self.get_width(), self.get_height())

    def _init_bar(self):
        self.canvas = Clutter.Canvas()
        self._resize_canvas()
        self.canvas.connect("draw", self.update_bar)
        self.set_content(self.canvas)

    def _init_transition(self):
        self.transition = Clutter.PropertyTransition.new('progress')
        self.transition.set_duration(500)

    def do_set_property(self, prop, value):
        self.progress = value

    def do_get_property(self, prop):
        return self.progress

    def update(self, new_progress, page, page_count):
        self.transition.set_from(self.progress)
        self.transition.set_to(new_progress)
        self.remove_transition('progress')
        self.add_transition('progress', self.transition)
        self.page = page
        self.page_count = page_count
        self.where = ''.join([str(self.page+1), '/', str(self.page_count)])

    def update_bar(self, canvas, context, width, height):
        context.scale(width, height)
        context.rectangle(0, 0, self.progress, 1)
        context.set_source_rgba(0, 0.894, 0.765, 1)
        context.fill()
        context.rectangle(self.progress, 0, 1, 1)
        context.set_source_rgba(0, 0, 0, 1)
        context.fill()
        return True


class SignedProgressBar(ProgressBar):
    def __init__(self, page_count='?', page=0):
        self.where = ''.join([str(page + 1), '/', str(page_count)])
        super().__init__()

    def update_bar(self, canvas, context, width, height):
        super().update_bar(canvas, context, width, height)
        context.set_font_size(1)
        context.set_source_rgb(255, 255, 255)
        context.select_font_face('Monospace', 0, 0)
        context.move_to(0.85, 0.9)
        context.scale(0.03, 1)  # text not stretched onto the whole bar
        context.show_text(self.where)
        return True


class PhotoSlide(Clutter.Actor):
    def __init__(self):
        super().__init__()
        self.image_actor = Mx.Image()
        self.add_child(self.image_actor)

    def set_model(self, model):
        self.model = model
        self.image_actor.set_from_file(self.model["photo_path"])
