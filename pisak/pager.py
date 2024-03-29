'''
Basic implementation of sliding page widget.
'''
from math import ceil

from gi.repository import Clutter, GObject
from pisak import properties, scanning, layout, unit


class DataSource(GObject.GObject):
    """
    Base class for Pisak data sources.
    """
    __gtype_name__ = "PisakPagerDataSource"
    __gproperties__ = {
        "tile_ratio_width": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "tile_ratio_height": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "tile_ratio_spacing": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "tile_preview_ratio_width": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "tile_preview_ratio_height": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        self.from_idx = 0
        self.to_idx = 0
        self.data_length = 0
        self.data = None
        self.tiles_handler = None

    @property
    def tile_ratio_height(self):
        return self._tile_ratio_height

    @tile_ratio_height.setter
    def tile_ratio_height(self, value):
        self._tile_ratio_height = value

    @property
    def tile_ratio_width(self):
        return self._tile_ratio_width

    @tile_ratio_width.setter
    def tile_ratio_width(self, value):
        self._tile_ratio_width = value

    @property
    def tile_ratio_spacing(self):
        return self._tile_ratio_spacing

    @tile_ratio_spacing.setter
    def tile_ratio_spacing(self, value):
        self._tile_ratio_spacing = value

    @property
    def tile_preview_ratio_height(self):
        return self._tile_preview_ratio_height

    @tile_preview_ratio_height.setter
    def tile_preview_ratio_height(self, value):
        self._tile_preview_ratio_height = value

    @property
    def tile_preview_ratio_width(self):
        return self._tile_preview_ratio_width

    @tile_preview_ratio_width.setter
    def tile_preview_ratio_width(self, value):
        self._tile_preview_ratio_width = value

    def _generate_tiles(self):
        raise NotImplementedError

    def get_tiles_forward(self, count):
        """
        Return given number of forward tiles generated from data.
        :param count: number of tiles to be returned
        """
        self.from_idx = self.to_idx % self.data_length
        self.to_idx = min(self.from_idx + count, self.data_length)
        return self._generate_tiles()

    def get_tiles_backward(self, count):
        """
        Return given number of backward tiles generated from data.
        :param count: number of tiles to be returned
        """
        self.to_idx = self.from_idx or self.data_length
        if self.to_idx < count:
            self.from_idx = self.data_length - count + self.to_idx
        else:
            self.from_idx = self.to_idx - count
        return self._generate_tiles()


class _Page(scanning.Group):
    """
    Page widget supplied to pager as its content.
    """
    def __init__(self, width, height, rows, columns, tiles, strategy, selector, ratio_spacing):
        super().__init__()
        self.set_size(width, height)
        self.strategy = strategy
        self.selector = selector
        layout = Clutter.BoxLayout()
        layout.set_spacing(unit.h(ratio_spacing))
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.set_layout_manager(layout)
        self.set_y_align(Clutter.ActorAlign.START)
        self._add_tiles(rows, columns, tiles, ratio_spacing)

    def _add_tiles(self, rows, columns, tiles, ratio_spacing):
        index = 0
        for _row in range(rows):
            group = scanning.Group()
            group.strategy = scanning.RowStrategy()
            group.selector = self.selector
            group.strategy.unwind_to = self
            group.strategy.max_cycle_count = self.strategy.max_cycle_count
            group.strategy.interval = self.strategy.interval
            group_box = layout.Box()
            group_box.ratio_spacing = ratio_spacing
            group.add_child(group_box)
            self.add_child(group)
            for _col in range(columns):
                if index < len(tiles):
                    actor = tiles[index]
                    group_box.add_child(actor)
                else:
                    actor = Clutter.Actor()
                    group_box.add_child(actor)
                    actor.set_x_expand(True)
                    actor.set_y_expand(True)
                index += 1


class _FlipGroup(scanning.Group):
    def __init__(self, pager):
        super().__init__()
        self.pager = pager
    
    def enable_hilite(self):
        self.pager.flip()
    
    def disable_hilite(self):
        pass


class PagerWidget(layout.Bin):
    """
    Pisak generic pager widget.
    Display elements placed on pages.
    Display only one page at time and is responsible for flipping them.
    """
    __gtype_name__ = "PisakPagerWidget"
    __gsignals__ = {
        "progressed": (
            GObject.SIGNAL_RUN_FIRST, None,
            (GObject.TYPE_FLOAT, GObject.TYPE_INT64)),
        "limit-declared": (
            GObject.SIGNAL_RUN_FIRST, None,
            (GObject.TYPE_INT64,))
    }
    __gproperties__ = {
        "data-source": (
            DataSource.__gtype__, "", "",
            GObject.PARAM_READWRITE),
        "rows": (
            GObject.TYPE_UINT, "", "", 1,
            GObject.G_MAXUINT, 4, GObject.PARAM_READWRITE),
        "columns": (
            GObject.TYPE_UINT, "", "", 1,
            GObject.G_MAXUINT, 3, GObject.PARAM_READWRITE),
        "page-strategy": (
            scanning.Strategy.__gtype__, "", "",
            GObject.PARAM_READWRITE),
        "page-selector": (
            GObject.TYPE_STRING, "", "",
            "mouse", GObject.PARAM_READWRITE),
        "page-ratio-spacing": (
            GObject.TYPE_FLOAT, None, None,
            0, 1., 0, GObject.PARAM_READWRITE),
        "idle-duration": (
            GObject.TYPE_INT64, "idle duration",
            "duration of one page exposition", 0,
            GObject.G_MAXUINT, 5000, GObject.PARAM_READWRITE),
        "transition-duration": (
            GObject.TYPE_INT64, "transition duration",
            "duration of page transition", 0,
            GObject.G_MAXUINT, 1000, GObject.PARAM_READWRITE)
    }

    def __init__(self, rows=3, columns=4):
        super().__init__()
        self.is_running = False
        self.set_clip_to_allocation(True)
        self.page_index = 0
        self.pages_count = 1
        self.old_page_transition = Clutter.PropertyTransition.new("x")
        self.new_page_transition = Clutter.PropertyTransition.new("x")
        self.new_page_transition.connect("stopped", self._clean_up)
        self.idle_duration = 3000
        self.transition_duration = 1000
        self._data_source = None
        self._page_strategy = None
        self._page_selector = "mouse"
        self._page_ratio_spacing = 0.01
        self._rows = rows
        self._columns = columns
        self._current_page = None
        self.old_page = None
        self.connect("notify::mapped", self._show_initial_page)

    @property
    def page_strategy(self):
        return self._page_strategy

    @page_strategy.setter
    def page_strategy(self, value):
        self._page_strategy = value

    @property
    def page_selector(self):
        return self._page_selector

    @page_selector.setter
    def page_selector(self, value):
        self._page_selector = value

    @property
    def page_ratio_spacing(self):
        return self._page_ratio_spacing

    @page_ratio_spacing.setter
    def page_ratio_spacing(self, value):
        self._page_ratio_spacing = value

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, value):
        self._data_source = value

    @property
    def rows(self):
        return self._rows
    
    @rows.setter
    def rows(self, value):
        self._rows = value
    
    @property
    def columns(self):
        return self._columns
    
    @columns.setter
    def columns(self, value):
        self._columns = value

    @property
    def idle_duration(self):
        return self._idle_duration

    @idle_duration.setter
    def idle_duration(self, value):
        self._idle_duration = value

    @property
    def transition_duration(self):
        return self.new_page_transition.get_duration()

    @transition_duration.setter
    def transition_duration(self, value):
        self.new_page_transition.set_duration(value)
        self.old_page_transition.set_duration(value)

    def _introduce_new_page(self, tiles, trans_desc=None):
        """
        Method for adding and displaying new page and disposing of the old one.
        :param tiles: list of tiles to be placed on the new page
        :param trans_desc: list of pages transitions parameters, that is:
        new page initial x coordinate, new page final x coordinate,
        old page final x coordinate; or None for initial page
        """
        if trans_desc is None:
            self._current_page = _Page(self.get_width(), self.get_height(),
                        self.rows, self.columns, tiles, self.page_strategy,
                        self.page_selector, self.page_ratio_spacing)
            self.add_child(self._current_page)
        else:
            self.old_page = self._current_page
            self._current_page = _Page(self.get_width(), self.get_height(),
                    self.rows, self.columns, tiles, self.page_strategy,
                    self.page_selector, self.page_ratio_spacing)
            self._current_page.set_x(trans_desc[0])
            self.add_child(self._current_page)
            self.new_page_transition.set_from(trans_desc[0])
            self.new_page_transition.set_to(trans_desc[1])
            self.old_page_transition.set_to(trans_desc[2])
            self.old_page.add_transition("x", self.old_page_transition)
            self._current_page.add_transition("x", self.new_page_transition)
        if self.pages_count > 0:
            self.emit("progressed", float(self.page_index+1) \
                    / self.pages_count, self.page_index+1)
        else:
            self.emit("progressed", 0, 0)

    def _show_initial_page(self, source, event):
        """
        Method being a 'notify::mapped' signal handler. Display pager
        initial page.
        """
        if self.data_source is not None and self._current_page is None:
            self.pages_count = ceil(self.data_source.data_length \
                                    / (self.rows*self.columns))
            self.emit("limit-declared", self.pages_count)
            tiles = self.data_source.get_tiles_forward(self.columns * self.rows)
            self._introduce_new_page(tiles)

    def _automatic_timeout(self, data):
        """
        Handler function for the automatic page flipping timeout.
        """
        if self.is_running:
            self.next_page()
            return True
        else:
            return False

    def _clean_up(self, source, event):
        """
        Func used as a signal handler. Clean up after stoppage of the
        new page 'x' transition. Remove transitions and
        free the old page.
        """
        self._current_page.remove_transition("x")
        self.old_page.remove_transition("x")
        if self.old_page is not None:
            if self.contains(self.old_page):
                self.remove_child(self.old_page)
        self.old_page = None

    def scan_page(self):
        """
        Start scanning the current page.
        """
        self.get_stage().pending_group = self._current_page

    def next_page(self):
        """
        Move to the next page.
        """
        if self.old_page is None and self.pages_count > 1:
            tiles = self.data_source.get_tiles_forward(self.columns * self.rows)
            self.page_index = (self.page_index+1) % self.pages_count
            self._introduce_new_page(tiles, [unit.size_pix[0],
                                        0, -1*unit.size_pix[0]])

    def previous_page(self):
        """
        Move to the previous page.
        """
        if self.old_page is None and self.pages_count > 1:
            if self.page_index == 0:
                count = self.data_source.data_length % \
                        ((self.pages_count - 1) * self.columns * self.rows) \
                        or self.columns * self.rows
            else:
                count = self.columns * self.rows
            tiles = self.data_source.get_tiles_backward(count)
            self.page_index = self.page_index - 1 if self.page_index >= 1 \
                                    else self.pages_count - 1
            self._introduce_new_page(tiles, [-1*unit.size_pix[0],
                                            0, unit.size_pix[0]])

    def run_automatic(self):
        """
        Start automatic page flipping.
        """
        self.is_running = True
        Clutter.threads_add_timeout(0, self.idle_duration, self._automatic_timeout, None)

    def stop_automatic(self):
        """
        Stop automatic page flipping.
        """
        self.is_running = False
