import os.path

from gi.repository import Mx, GObject, Clutter

from pisak import widgets, layout, res, pager, properties, unit
from pisak.viewer import database_agent, image


class SlideShow(layout.Bin):
    __gtype_name__ = "PisakViewerSlideShow"
    __gsignals__ = {
        "progressed": (GObject.SIGNAL_RUN_FIRST, None, (GObject.TYPE_FLOAT,)),
        "limit-set": (GObject.SIGNAL_RUN_FIRST, None, (GObject.TYPE_INT64,))
    }
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
        "slideshow_fullscreen": (
            GObject.TYPE_BOOLEAN, "if fullscreen",
            "if slideshow on fullscreen", False,
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        self.index = 0
        self.new_slide_transition = Clutter.PropertyTransition.new("x")
        self.new_slide_transition.connect("stopped", self.clean_up)
        self.old_slide_transition = Clutter.PropertyTransition.new("x")
        self.transition_duration = 1000
        self.idle_duration = 1000
        self.slideshow_fullscreen = True
        self.new_slide = None
        self.slide = None
        self.stage = None
        self.slideshow_on = False
        self.fullscreen_on = False
        self.album_length = None
        self.set_clip_to_allocation(True)

    @property
    def data_source(self):
        return self._data_source

    @data_source.setter
    def data_source(self, value):
        self._data_source = value

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

    @property
    def slideshow_fullscreen(self):
        return self._slideshow_fullscreen

    @slideshow_fullscreen.setter
    def slideshow_fullscreen(self, value):
        self._slideshow_fullscreen = value

    def show_initial_slide(self, initial_index=0):
        self.album_length = len(self.data_source.slides)
        self.emit("limit-set", self.album_length)
        if initial_index is None:
            self.index = 0
        else:
            self.index = initial_index
        if self.data_source is not None:
            self.slide = self.data_source.slides[self.index]
            self.add_child(self.slide)
        self.emit("progressed", float(self.index / self.album_length))
        
    def slideshow_timeout(self, *args):
        if self.slideshow_on:
            self.next_slide()
            return True
        else:
            return False

    def next_slide(self, *args):
        if self.new_slide is None:
            self.index = (self.index + 1) % self.album_length
            self.new_slide = self.data_source.slides[self.index]
            self.new_slide.set_x(unit.size_pix[0])
            self.new_slide_transition.set_from(unit.size_pix[0])
            self.new_slide_transition.set_to(0)
            self.old_slide_transition.set_to(-1*unit.size_pix[0])
            if self.fullscreen_on:
                self.cover_frame.add_child(self.new_slide)
                self.new_slide.set_size(unit.size_pix[0], unit.size_pix[1])
            else:
                self.add_child(self.new_slide)
            self.slide.add_transition("x", self.old_slide_transition)
            self.new_slide.add_transition("x", self.new_slide_transition)
            self.emit("progressed", float(self.index / self.album_length))
        
    def previous_slide(self):
        if self.new_slide is None:
            self.index = self.index - 1 if self.index > 0 else self.album_length - 1
            self.new_slide = self.data_source.slides[self.index]
            self.new_slide.set_x(-1*unit.size_pix[0])
            self.new_slide_transition.set_from(-1*unit.size_pix[0])
            self.new_slide_transition.set_to(0)
            self.old_slide_transition.set_to(unit.size_pix[0])
            if self.fullscreen_on:
                self.cover_frame.add_child(self.new_slide)
                self.new_slide.set_size(unit.size_pix[0], unit.size_pix[1])
            else:
                self.add_child(self.new_slide)
            self.slide.add_transition("x", self.old_slide_transition)
            self.new_slide.add_transition("x", self.new_slide_transition)
            self.emit("progressed", float(self.index / self.album_length))

    def clean_up(self, *args):
        if self.slide is not None:
            if self.contains(self.slide):
                self.remove_child(self.slide)
            elif self.slideshow_fullscreen:
                if self.cover_frame.contains(self.slide):
                    self.cover_frame.remove_child(self.slide)
        self.slide = self.new_slide
        self.slide_width, self.slide_height = self.slide.get_size()
        self.new_slide = None
        self.slide.remove_transition("x")

    def run(self):
        if self.slideshow_fullscreen is True:
            self.fullscreen_on = True
            self.stage = self.get_stage()
            self.cover_frame = Clutter.Actor()
            self.cover_frame.set_size(unit.size_pix[0], unit.size_pix[1])
            self.slide_width, self.slide_height = self.slide.get_size()
            self.remove_child(self.slide)
            self.cover_frame.add_child(self.slide)
            self.cover_frame.set_background_color(Clutter.Color.new(0, 0, 0, 255))
            self.cover_frame.connect("button-press-event", self.stop)
            self.slide.set_size(unit.size_pix[0], unit.size_pix[1])
            self.stage.add_child(self.cover_frame)
            self.hide()
        self.slideshow_on = True
        Clutter.threads_add_timeout(0, self.idle_duration, self.slideshow_timeout, None)

    def stop(self, *args):
        self.slideshow_on = False
        if self.slideshow_fullscreen is True:
            self.fullscreen_on = False
            self.show()
            self.stage.remove_child(self.cover_frame)
            self.cover_frame.remove_child(self.slide)
            self.slide.set_width(self.slide_width)
            self.slide.set_height(self.slide_height)
            self.add_child(self.slide)
        

class PhotoSlidesSource(pager.DataSource, properties.PropertyAdapter):
    __gtype_name__ = "PisakViewerPhotoSlidesSource"
    __gproperties__ = {
        "slide_ratio_width": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "slide_ratio_height": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.slide_ratio_height = 0.7
        self.slide_ratio_width = 0.68
        self.slides = []
        self.album = None

    @property
    def slide_ratio_width(self):
        return self._slide_ratio_width

    @slide_ratio_width.setter
    def slide_ratio_width(self, value):
        self._slide_ratio_width = value

    @property
    def slide_ratio_height(self):
        return self._slide_ratio_height

    @slide_ratio_height.setter
    def slide_ratio_height(self, value):
        self._slide_ratio_height = value

    @property
    def album(self):
        return self._album

    @album.setter
    def album(self, value):
        self._album = value
        if value is not None:
            self._generate_slides()

    def _generate_slides(self):
        self.data = database_agent.get_photos_from_category(self.album)
        for item in self.data:
            slide = PhotoSlide()
            slide.ratio_height = self.slide_ratio_height
            slide.ratio_width = self.slide_ratio_width
            slide.photo_path = item["path"]
            self.slides.append(slide)


class LibraryTilesSource(pager.DataSource, properties.PropertyAdapter):
    __gtype_name__ = "PisakViewerLibraryTilesSource"
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
        super().__init__()
        self.tiles = []
        self.index = 0
        self._generate_tiles()

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
        self.data = database_agent.get_categories()
        for item in self.data:
            tile = PhotoTile()
            tile.label_text = item["category"]
            tile.preview_path = database_agent.get_preview_of_category(item["category"])["path"]
            tile.ratio_width = self.tile_ratio_width
            tile.ratio_height = self.tile_ratio_height
            tile.ratio_spacing = self.tile_ratio_spacing
            tile.preview_ratio_height = self.tile_preview_ratio_height
            tile.preview_ratio_widtht = self.tile_preview_ratio_width
            self.tiles.append(tile)
            
    def get_tiles(self, count):
        tiles = self.tiles[self.index : count]
        self.index = (self.index + count) % len(self.tiles) if len(self.tiles) > 0 else self.index
        return tiles


class AlbumTilesSource(LibraryTilesSource):
    __gtype_name__ = "PisakViewerAlbumTilesSource"

    def __init__(self):
        self.album = None
        super().__init__()

    @property
    def album(self):
        return self._album

    @album.setter
    def album(self, value):
        self._album = value
        if value is not None:
            self._generate_tiles()

    def _generate_tiles(self):
        if self.album is not None:
            self.data = database_agent.get_photos_from_category(self.album)
            for item in self.data:
                tile = PhotoTile()
                tile.preview_path = item["path"]
                tile.scale_mode = Mx.ImageScaleMode.FIT
                tile.ratio_width = self.tile_ratio_width
                tile.ratio_height = self.tile_ratio_height
                self.tiles.append(tile)
        

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
        
