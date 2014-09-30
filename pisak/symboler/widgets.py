"""
Module with widgets specific to symboler application.
"""
from gi.repository import Mx

from pisak import widgets, pager
from pisak.res import colors
from pisak.symboler import database_manager


class TilesSource(pager.DataSource):
    """
    Data source generating tiles with symbols.
    """
    __gtype_name__ = "PisakSymbolerTilesSource"
    
    def __init__(self):
        super().__init__()
        self.index = 0
        self.data = database_manager.get_all_symbols()

    def _generate_tiles(self, count):
        tiles = []
        for index in range(self.index, self.index + count):
            if index < len(self.data):
                tile = widgets.PhotoTile()
                tile.hilite_tool = widgets.Aperture()
                tile.set_background_color(colors.LIGHT_GREY)
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
