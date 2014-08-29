import os.path

from gi.repository import Mx, GObject, Clutter

from pisak import widgets, layout, res, pager, properties, unit
from pisak.viewer import database_agent, image


class SlideShow(layout.Bin):
    __gtype_name__ = "PisakViewerSlideShow"
    __gproperties__ = {
        "data-source": (
            pager.DataSource.__gtype__, "", "", GObject.PARAM_READWRITE),
        "transition-duration": (
            GObject.TYPE_INT64, "transition duration",
            "duration of slides transition", 0,
            GObject.G_MAXUINT, 1000, GObject.PARAM_READWRITE),
        "idle-duration": (
            GObject.TYPE_INT64, "idle duration",
            "duration of one slide exposition", 0,
            GObject.G_MAXUINT, 5000, GObject.PARAM_READWRITE),
    }

    def __init__(self):
        self.index = 0
        self.new_slide_transition = Clutter.PropertyTransition.new("x")
        self.new_slide_transition.connect("stopped", self.clean_up)
        self.old_slide_transition = Clutter.PropertyTransition.new("x")
        self.transition_duration = 1000
        self.idle_duration = 1000
        self.new_slide = None
        self.slide = None
        self.slideshow_on = False
        self.album_length = None

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, value):
        self._data_source = value
        if value is not None:
            self.album_length = len(value.get_data())

    @property
    def transition_duration(self):
        return self.new_slide_transition.get_duration()

    @transition_duration.setter
    def transition_duration(self, value):
        self.new_slide_transition.set_duration(value)
        self.old_slide_transition.set_duration(value)

    @property
    def idle_duration(self):
        return self._idle_duration

    @idle_duration.setter
    def idle_duration(self, value):
        self._idle_duration = value

    def show_initial_slide(self, initial_index=0):
        if initial_index is None:
            self.index = 0
        else:
            self.index = initial_index
        if self.data_source is not None:
            self.slide = self.data_source.get_data()[self.index]
            self.add_child(self.slide)

    def slideshow_timeout(self, *args):
        if self.slideshow_on:
            self.next_slide()
            return True
        else:
            return False

    def next_slide(self, *args):
        self.index = (self.index + 1) % self.album_length
        if self.new_slide is None:
            self.new_slide = self.data_source.get_data()[self.index]
            self.new_slide.set_x(unit.size_pix[0])
            self.new_slide_transition.set_from(unit.size_pix[0])
            self.new_slide_transition.set_to(0)
            self.old_slide_transition.set_to(-1*unit.size_pix[0])
            self.add_child(self.new_slide)
            self.slide.add_transition("x", self.old_slide_transition)
            self.new_slide.add_transition("x", self.new_slide_transition)
        
    def previous_slide(self):
        self.index = self.index - 1 if self.index > 0 else self.album_length - 1
        if self.new_slide is None:
            self.new_slide = self.data_source.get_data()[self.index]
            self.new_slide.set_x(-1*unit.size_pix[0])
            self.new_slide_transition.set_from(-1*unit.size_pix[0])
            self.new_slide_transition.set_to(0)
            self.old_slide_transition.set_to(unit.size_pix[0])
            self.add_child(self.new_slide)
            self.slide.add_transition("x", self.old_slide_transition)
            self.new_slide.add_transition("x", self.new_slide_transition)

    def clean_up(self, *args):
        if self.slide is not None:
            if self.contains(self.slide):
                self.remove_child(self.slide)
        self.slide = self.new_slide
        self.new_slide = None
        self.slide.remove_transition("x")

    def run(self):
        self.slideshow_on = True
        Clutter.threads_add_timeout(0, self.idle_duration, self.slideshow_timeout, None)

    def stop(self):
        self.slideshow_on = False
        

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
        self.slide_ratio_height = 0.7
        self.slide_ratio_width = 0.68
        self.tile_ratio_spacing = 0.01
        self.tile_preview_ratio_width = 0.12
        self.tile_preview_ratio_height = 0.12
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
                self.tiles.append(tile)

    def _generate_slides(self):
        if self.album is not None:
            data = database_agent.get_photos_from_category(self.album)
            for item in data:
                slide = PhotoSlide()
                slide.ratio_height = self.slide_ratio_height
                slide.ratio_width = self.slide_ratio_width
                slide.photo_path = item["path"]
                self.tiles.append(slide)

    def get_data(self):
        return self.tiles
            
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
        self.image_buffer = None
        self.photo = Mx.Image()
        self.photo.set_scale_mode(Mx.ImageScaleMode.FIT)
        self.add_child(self.photo)

    @property
    def photo_path(self):
        return self._photo_path

    @photo_path.setter
    def photo_path(self, value):
        self._photo_path = value
        absolute_path = os.path.join(self.MODEL["photo_path"], value)
        self.photo.set_from_file(absolute_path)
        self.image_buffer = image.PhotoBuffer(absolute_path, self)

    @property
    def transition_duration(self):
        return self.photo.get_transition_duration()

    @transition_duration.setter
    def transition_duration(self, value):
        self.photo.set_transition_duration(value)

    def set_from_data(self, data, mode, width, height, row_stride):
        self.photo.set_from_data(data, mode, width, height, row_stride)
        
