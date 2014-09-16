'''
Basic implementation of sliding page widget.
'''
from math import ceil

from gi.repository import Clutter, GObject
from pisak import properties, scanning, layout, unit


class DataSource(GObject.GObject):
    def get_tiles(self, count):
        return []


class _Page(scanning.Group):
    def __init__(self, rows, columns, tiles, strategy, selector, ratio_spacing):
        super().__init__()
        self.set_x_expand(True)
        self.set_y_expand(True)
        self.set_y_align(Clutter.ActorAlign.START)
        self.strategy = strategy
        self.selector = selector
        self._add_tiles(rows, columns, tiles, selector, ratio_spacing)
        layout = Clutter.BoxLayout()
        layout.set_spacing(unit.h(ratio_spacing))
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.set_layout_manager(layout)

    def _add_tiles(self, rows, columns, tiles, selector, ratio_spacing):
        index = 0
        for _row in range(rows):
            if index >= len(tiles):
                return
            group = scanning.Group()
            group.strategy = scanning.RowStrategy()
            group.strategy.max_cycle_count = 2
            group.selector = selector
            group_box = Clutter.Actor()
            group_box_layout = Clutter.BoxLayout()
            group_box_layout.set_spacing(unit.w(ratio_spacing))
            group_box.set_layout_manager(group_box_layout)
            group.add_child(group_box)
            self.add_child(group)
            for _col in range(columns):
                if index < len(tiles):
                    actor = tiles[index]
                    group_box.add_child(actor)
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
    }

    def __init__(self, rows=3, columns=4):
        super().__init__()
        self.is_running = False
        self.page_index = 0
        self.pages_count = 1
        self.idle_duration = 3000
        self._data_source = None
        self._page_strategy = None
        self._page_selector = None
        self._page_ratio_spacing = None
        self._rows = rows
        self._columns = columns
        self._current_page = None
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
    
    def _show_initial_page(self, source, event):
        if self.data_source is not None and self._current_page is None:
            self.pages_count = ceil(len(self.data_source.data) \
                                    / (self.rows*self.columns))
            self.emit("limit-declared", self.pages_count)
            if self.pages_count > 0:
                self.emit("progressed", float(self.page_index+1) \
                        / self.pages_count,
                        self.page_index+1)
            else:
                self.emit("progressed", 0, 0)
            tiles = self.data_source.get_tiles(self.columns * self.rows)
            if len(tiles) > 0:
                self._current_page = _Page(self.rows, self.columns, tiles,
                    self.page_strategy, self.page_selector, self.page_ratio_spacing)
                self.add_child(self._current_page)

    def scan_page(self):
        """
        Start scanning the current page.
        """
        self.get_stage().pending_group = self._current_page

    def next_page(self):
        """
        Move to the next page.
        """
        if self.pages_count > 1:
            tiles = self.data_source.get_tiles(self.columns * self.rows)
            if len(tiles) > 0:
                self.page_index = (self.page_index+1) % self.pages_count
                _new_page = _Page(self.rows, self.columns, tiles,
                    self.page_strategy, self.page_selector, self.page_ratio_spacing)
                self.remove_child(self._current_page)
                self.add_child(_new_page)
                self._current_page = _new_page
                self.emit("progressed", float(self.page_index+1) \
                        / self.pages_count,
                        self.page_index+1)

    def automatic_timeout(self, data):
        """
        Handler function for the automatic page flipping timeout.
        """
        if self.is_running:
            self.next_page()
            return True
        else:
            return False

    def run_automatic(self):
        """
        Start automatic page flipping.
        """
        self.is_running = True
        Clutter.threads_add_timeout(0, self.idle_duration, self.automatic_timeout, None)

    def stop_automatic(self):
        """
        Stop automatic page flipping.
        """
        self.is_running = False
