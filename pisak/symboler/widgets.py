"""
Module with widgets specific to symboler application.
"""
import os.path

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
        self.text_buffer = []
        self.scrolled_content_left = []
        self.scrolled_content_right = []
        self.set_x_align(Clutter.ActorAlign.START)
        self.connect("notify::allocation", self._on_allocation_update)

    def _on_allocation_update(self, source, event):
        self.border_x = self.get_abs_allocation_vertices()[1].x

    def _check_content_extent(self, new_symbol):
        endmost_symbol = self.get_last_child()
        # if newly appended symbol would extent over the self allocation area:
        if endmost_symbol is not None:
            if (endmost_symbol.get_abs_allocation_vertices()[1].x +
                self.layout.get_spacing() + new_symbol.get_width()) \
                    > self.border_x:
                if len(self.scrolled_content_right) > 0:
                    while self.scrolled_content_right:
                        self.scroll_content_left()
                self.scroll_content_left()

    def _restore_scrolled_content_left(self):
        if len(self.scrolled_content_left) > 0:
            symbol_to_restore = self.scrolled_content_left.pop()
            self.insert_child_below(symbol_to_restore, None)

    def _restore_scrolled_content_right(self):
        if len(self.scrolled_content_right) > 0:
            symbol_to_restore = self.scrolled_content_right.pop()
            self.insert_child_above(symbol_to_restore, None)

    def _generate_symbol(self, model):
        symbol = widgets.PhotoTile()
        symbol.label.set_style_class("PisakSymbolerPhotoTileLabel")
        symbol.label_text = model.label_text
        symbol.set_y_expand(True)
        symbol.ratio_width = model.ratio_width
        symbol.ratio_spacing = model.ratio_spacing
        symbol.preview_ratio_width = model.preview_ratio_width
        symbol.preview_ratio_height = model.preview_ratio_height
        symbol.scale_mode = Mx.ImageScaleMode.FIT
        symbol.preview_path = model.preview_path
        return symbol

    def scroll_content_left(self):
        """
        Scroll self content backward.
        """
        first_symbol = self.get_child_at_index(0)
        if first_symbol is not None:
            self.scrolled_content_left.append(first_symbol)
            self.remove_child(first_symbol)
        self._restore_scrolled_content_right()

    def scroll_content_right(self):
        """
        Scroll self content foreward.
        """
        endmost_symbol = self.get_last_child()
        if endmost_symbol is not None:
            self.scrolled_content_right.append(endmost_symbol)
            self.remove_child(endmost_symbol)
        self._restore_scrolled_content_left()

    def append_symbol(self, tile):
        """
        Append symbol to the entry.
        :param tile: instance of PisakPhotoTile containing preview_path field
        """
        symbol = self._generate_symbol(tile)
        self.text_buffer.append(tile.label_text)
        self._check_content_extent(symbol)
        self.insert_child_above(symbol, None)

    def delete_symbol(self):
        """
        Delete the last symbol from the entry.
        """
        if len(self.scrolled_content_right) > 0:
            while self.scrolled_content_right:
                self.scroll_content_left()
        endmost_symbol = self.get_last_child()
        if endmost_symbol is not None:
            self.remove_child(endmost_symbol)
            self.text_buffer.pop()
        self._restore_scrolled_content_left()

    def get_text(self):
        """
        Return string containing current text buffer.
        """
        return " ".join(self.text_buffer)

    def clear_all(self):
        """
        Clear the entry, delete all symbols.
        """
        self.remove_all_children()
    

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
                item = self.data[index]
                tile = widgets.PhotoTile()
                tile.label.set_style_class("PisakSymbolerPhotoTileLabel")
                if item.text:
                    label = item.text
                else:
                    label = os.path.splitext(os.path.split(item.path)[-1])[0]
                tile.label_text = label
                tile.hilite_tool = widgets.Aperture()
                tile.connect("activate", lambda source, tile:
                             self.target.append_symbol(tile), tile)
                tile.set_background_color(colors.LIGHT_GREY)
                tile.ratio_width = self.tile_ratio_width
                tile.ratio_height = self.tile_ratio_height
                tile.ratio_spacing = self.tile_ratio_spacing
                tile.preview_ratio_width = self.tile_preview_ratio_width
                tile.preview_ratio_height = self.tile_preview_ratio_height
                tile.scale_mode = Mx.ImageScaleMode.FIT
                tile.preview_path = item.path
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
