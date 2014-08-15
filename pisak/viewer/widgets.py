from gi.repository import Clutter, Mx, GObject

from pisak import layout, properties, unit


class ProgressBarBar(Mx.ProgressBar):
    __gtype_name__ = "PisakViewerProgressBarBar"

        
class ProgressBarLabel(Mx.Label):
    __gtype_name__ = "PisakViewerProgressBarLabel"


class PhotoTileLabel(Mx.Label):
    __gtype_name__ = "PisakViewerPhotoTileLabel"
