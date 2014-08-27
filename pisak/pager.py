'''
Basic implementation of sliding page widget.
'''
from gi.repository import Clutter, GObject
from pisak import properties, scanning


class DataSource(GObject.GObject):
    def get_tiles(self, count):
        return []


class _Page(Clutter.Actor):    
    def __init__(self, rows, columns, tiles):
        super().__init__()
        self._add_tiles(rows, columns, tiles)
        self.set_layout_manager(Clutter.BoxLayout())

    def _add_tiles(self, rows, columns, tiles):
        index = 0
        for _column in range(columns):
            group = scanning.Group()
            group_box = Clutter.Actor()
            group_box_layout = Clutter.BoxLayout()
            group_box_layout.set_orientation(Clutter.Orientation.VERTICAL)
            group_box.set_layout_manager(group_box_layout)
            group.add_child(group_box)
            self.add_child(group)
            for _row in range(rows):
                actor = tiles[index] if index < len(tiles) else Clutter.Actor()
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


class PagerWidget(Clutter.Actor, properties.PropertyAdapter):
    __gtype_name__ = "PisakPagerWidget"

    __gproperties__ = {
        "data-source": (DataSource.__gtype__, "", "", GObject.PARAM_READWRITE),
        "rows": (GObject.TYPE_UINT, "", "", 1, GObject.G_MAXUINT, 4, GObject.PARAM_READWRITE),
        "columns": (GObject.TYPE_UINT, "", "", 1, GObject.G_MAXUINT, 3, GObject.PARAM_READWRITE),
    }

    def __init__(self):
        super().__init__()
        self._data_source = None
        self._rows = 4
        self._columns = 3
        self._current_page = None
        self._flip_group = _FlipGroup(self)
        self.add_child(self._flip_group)

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, value):
        self._data_source = value
        self.flip()
    
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
    
    def flip(self):
        if self.data_source is not None:
            tiles = self.data_source.get_tiles(12)
        else:
            tiles = []
        if self._current_page is not None:
            self.remove_actor(self._current_page)
        self._current_page = _Page(self.rows, self.columns, tiles)
        self.add_child(self._current_page)
