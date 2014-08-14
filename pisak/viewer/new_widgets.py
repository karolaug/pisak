from gi.repository import Clutter, Mx, GObject

from pisak import layout, properties


class ProgressBar(layout.Bin, properties.PropertyAdapter):
    __gtype_name__ = "PisakProgressBar"
    __groperties__ = {
        "progress": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "label_ratio_x_offset": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE)
    }
    MODEL = {
        "label": "10 / 100",
        "label_ratio_x_offset": 0.7,
        "progress": 0.3
    }
    
    class Bar(Mx.ProgressBar):
        __gtype_name__ = "PisakViewerProgressBar"
        def __init__(self):
            super().__init__()
            
    class Label(Mx.Label):
        __gtype_name__ = "PisakViewerProgressBarLabel"
        def __init__(self):
            super().__init__()

    def __init__(self):
        super().__init__()
        self.label_ratio_x_offset = None
        self.bar = ProgressBar.Bar()
        self.label = ProgressBar.Label()
        self._display_bar()
        self._display_label()
        self.connect("notify::size", self._allocate_label)
        
        self._update_label(self.MODEL["label"])
        self.progress = self.MODEL["progress"]
        self.label_ratio_x_offset = self.MODEL["label_ratio_x_offset"]

    @property
    def progress(self):
        return self.bar.get_progress()

    @progress.setter
    def progress(self, value):
        self.bar.set_progress(value)

    @property
    def label_ratio_x_offset(self):
        return self._label_ratio_x_offset

    @label_ratio_x_offset.setter
    def label_ratio_x_offset(self, value):
        self._label_ratio_x_offset = value
        self._allocate_label()

    def _display_label(self):
        self.label.set_y_expand(True)
        self.label.set_y_align(Clutter.ActorAlign.START)
        self.add_child(self.label)

    def _display_bar(self):
        self.bar.set_x_expand(True)
        self.bar.set_y_expand(True)
        self.add_child(self.bar)

    def _allocate_label(self, *args):
        if self.get_width() and self.label_ratio_x_offset is not None:
            px_x_offset = self.label_ratio_x_offset * self.get_width()
            self.label.set_x(px_x_offset)

    def _update_label(self, value):
        self.label.set_text(value)
