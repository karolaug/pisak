"""
Module with widgets specific to symboler application.
"""
from gi.repository import Mx, Clutter, GObject

from pisak import widgets, pager, properties, layout
from pisak.res import colors
from pisak.symboler import database_manager


class Entry(layout.Box):
    """
    Entry window for typing symbols.
    """
    __gtype_name__ = "PisakSymbolerEntry"

    def __init__(self):
        super().__init__()
        self.set_x_align(Clutter.ActorAlign.START)

    def append_symbol(self, tile):
        """
        Add symbol to the end of the current symbols buffer.
        :param tile: instance of PisakPhotoTile containing preview_path field
        """
        symbol = Mx.Image()
        symbol.set_from_file(tile.preview_path)
        self.insert_child_below(symbol, None)


class TilesSource(pager.DataSource, properties.PropertyAdapter):
    """
    Data source generating tiles with symbols.
    """
    __gtype_name__ = "PisakSymbolerTilesSource"
    __gproperties__ = {
        "target": (
            Entry.__gtype__,
            "symbol inserting target",
            "id of entry to insert symbols",
            GObject.PARAM_READWRITE)
    }
    
    def __init__(self):
        super().__init__()
        self.index = 0
        self.data = database_manager.get_all_symbols()
        self.data_length = len(self.data)

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    def _generate_tiles(self, count):
        tiles = []
        for index in range(self.index, self.index + count):
            if index < len(self.data):
                tile = widgets.PhotoTile()
                tile.hilite_tool = widgets.Aperture()
                tile.connect("activate", lambda source, tile:
                             self.target.append_symbol(tile), tile)
                tile.set_background_color(colors.LIGHT_GREY)
                tile.ratio_width = self.tile_ratio_width
                tile.ratio_height = self.tile_ratio_height
                tile.scale_mode = Mx.ImageScaleMode.FIT
                tile.preview_path = self.data[index].path
            else:
                tile = Clutter.Actor()
            tiles.append(tile)
        return tiles

    def get_tiles(self, count):
        tiles = self._generate_tiles(count)
        self.index += count
        if self.index > len(self.data):
            self.index = 0
        return tiles
