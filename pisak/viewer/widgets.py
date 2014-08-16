from gi.repository import Mx

from pisak import widgets


class ProgressBarBar(Mx.ProgressBar):
    __gtype_name__ = "PisakViewerProgressBarBar"

        
class ProgressBarLabel(Mx.Label):
    __gtype_name__ = "PisakViewerProgressBarLabel"


class PhotoTileLabel(Mx.Label):
    __gtype_name__ = "PisakViewerPhotoTileLabel"


class Button(widgets.Button):
    __gtype_name__ = "PisakViewerButton"
