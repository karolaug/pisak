from gi.repository import Mx

from pisak import widgets, layout


class ProgressBarBar(Mx.ProgressBar):
    __gtype_name__ = "PisakViewerProgressBarBar"

        
class ProgressBarLabel(Mx.Label):
    __gtype_name__ = "PisakViewerProgressBarLabel"


class PhotoTileLabel(Mx.Label):
    __gtype_name__ = "PisakViewerPhotoTileLabel"


class Button(widgets.Button):
    __gtype_name__ = "PisakViewerButton"


class PhotoSlide(layout.Bin):
    __gtype_name__ = "PisakViewerPhotoSlide"
    __groperties__ = {
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

    def __init__(self):
        super().__init()
        self.photo = Mx.Image()
        self.photo.set_scale_mode(Mx.ImageScaleMode.FIT)
        self.add_child(self.photo)

    @property
    def photo_path(self):
        return self._photo_path

    @photo_path.setter
    def photo_path(self, value):
        self._photo_path = value
        self.photo.set_from_file(value)

    @property
    def transition_duration(self):
        return self.photo.get_transition_duration()

    @transition_duration.setter
    def transition_duration(self, value):
        self.photo.set_transition_duration(value)

    def set_from_data(self, data, mode, width, height, row_stride):
        self.photo.set_from_data(data, mode, width, height, row_stride)
        
