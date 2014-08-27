import os.path

from gi.repository import Mx, GObject

from pisak import widgets, layout, res, pager, properties
from pisak.viewer import database_agent


class DataSource(pager.DataSource, properties.PropertyAdapter):
    __gtype_name__ = "PisakViewerDataSource"
    __gproperties__ = {
        "data_type": (
            GObject.TYPE_STRING,
            "data type",
            "type of the data",
            "noop",
            GObject.PARAM_READWRITE),
        "album": (
            GObject.TYPE_STRING,
            "album name",
            "category of the photos",
            "noop",
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        self.data_generators = {"library": self._generate_library,
                                "album": self._generate_album,
                                "slideshow": self._generate_slides}
        self.album = None
        self.data_type = None
        self.tile_ratio_height = 0.2
        self.tile_ratio_width = 0.15
        self.tile_ratio_spacing = 0.01
        self.tile_preview_ratio_width = 0.12
        self.tile_preview_ratio_height = 0.7
        self.tiles = []
        self.index = 0

    @property
    def album(self):
        return self._album

    @album.setter
    def album(self, value):
        self._album = value

    @property
    def data_type(self):
        return self._data_type

    @data_type.setter
    def data_type(self, value):
        self._data_type = value
        if value in self.data_generators.keys():
            self.data_generators[value]()

    def _generate_library(self):
        data = database_agent.get_categories()
        for item in data:
            tile = PhotoTile()
            tile.label_text = item["category"]
            tile.preview_path = database_agent.get_preview_of_category(item["category"])["path"]
            tile.ratio_width = self.tile_ratio_width
            tile.ratio_height = self.tile_ratio_height
            tile.ratio_spacing = self.tile_ratio_spacing
            tile.preview_ratio_height = self.tile_preview_ratio_height
            tile.preview_ratio_widtht = self.tile_preview_ratio_width
            #tile.connect("clicked", enter_album, item["category"])
            self.tiles.append(tile)

    def _generate_album(self):
        if self.album is not None:
            data = database_agent.get_photos_from_category(self.album)
            for item in data:
                tile = PhotoTile()
                tile.preview_path = item["path"]
                tile.scale_mode = Mx.ImageScaleMode.FIT
                tile.ratio_width = self.tile_ratio_width
                tile.ratio_height = self.tile_ratio_height
                #tile.connect("clicked", enter_slideshow, item, self.album)
                self.tiles.append(tile)

    def _generate_slides(self):
        if self.album is not None:
            data = database_agent.get_photos_from_category(self.album)
            for item in data:
                slide = PhotoSlide()
                slide.photo_path = item["path"]
                #tile.connect("clicked", enter_slideshow, item, self.album)
                self.tiles.append(slide)
            
    def get_tiles(self, count):
        tiles = self.tiles[self.index : count]
        self.index = (self.index + count) % len(self.tiles)
        return tiles
        

class ProgressBar(widgets.NewProgressBar):
    __gtype_name__ = "PisakViewerProgressBar"
    
    def __init__(self):
        super().__init__()
        self.label = Mx.Label()
        self.label.set_style_class("PisakViewerProgressBar")
        self.bar.get_children()[0].set_style_class("PisakViewerProgressBar")
        self.bar.set_style_class("PisakViewerProgressBar")


class PhotoTile(widgets.PhotoTile):
    __gtype_name__ = "PisakViewerPhotoTile"
    
    def __init__(self):
        super().__init__()
        self.label = Mx.Label()
        self.label.set_style_class("PisakViewerPhotoTile")


class Button(widgets.Button):
    __gtype_name__ = "PisakViewerButton"


class PhotoSlide(layout.Bin):
    __gtype_name__ = "PisakViewerPhotoSlide"
    __gproperties__ = {
        "photo_path": (
            GObject.TYPE_STRING,
            "path to photo",
            "path to photo slide",
            "noop",
            GObject.PARAM_READWRITE),
        "transition_duration": (
            GObject.TYPE_INT64, "transition duration",
            "duration of photo transition", 0,
            GObject.G_MAXUINT, 500, GObject.PARAM_READWRITE)
    }
    MODEL = {
        "photo_path": res.PATH
    }

    def __init__(self):
        super().__init__()
        self.photo = Mx.Image()
        self.photo.set_scale_mode(Mx.ImageScaleMode.FIT)
        self.add_child(self.photo)

    @property
    def photo_path(self):
        return self._photo_path

    @photo_path.setter
    def photo_path(self, value):
        self._photo_path = value
        self.photo.set_from_file(os.path.join(self.MODEL["photo_path"], value))

    @property
    def transition_duration(self):
        return self.photo.get_transition_duration()

    @transition_duration.setter
    def transition_duration(self, value):
        self.photo.set_transition_duration(value)

    def set_from_data(self, data, mode, width, height, row_stride):
        self.photo.set_from_data(data, mode, width, height, row_stride)
        
