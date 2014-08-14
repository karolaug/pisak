from gi.repository import Clutter, Mx, GObject

from pisak import layout, properties


class ProgressBar(layout.Bin, properties.PropertyAdapter):
    class Bar(Mx.ProgressBar):
        __gtype_name__ = "PisakViewerProgressBarBar"
        
    class Label(Mx.Label):
        __gtype_name__ = "PisakViewerProgressBarLabel"


    __gtype_name__ = "PisakViewerProgressBar"
    __gproperties__ = {
        "progress": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "label_ratio_x_offset": (
            GObject.TYPE_FLOAT, None, None, 0, 1., 0,
            GObject.PARAM_READWRITE)
    }  

    def __init__(self):
        super().__init__()
        self.label_ratio_x_offset = None
        self.bar = ProgressBar.Bar()
        self.label = ProgressBar.Label()
        self._display_bar()
        self._display_label()
        self.connect("notify::width", self._allocate_label)

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


class Tile(layout.Bin, properties.PropertyAdapter):
    class Label(Mx.Label):
         __gtype_name__ = "PisakViewerTileLabel"

         
    __gtype_name__ = "PisakViewerTile"
    __gsignals__ = {
        "activate": (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    __gproperties__ = {
        "preview_path": (
            GObject.TYPE_STRING,
            "path to preview photo",
            "path to preview photo displayed on a tile",
            "noop",
            GObject.PARAM_READWRITE),
        "label_text": (
            GObject.TYPE_STRING,
            "label under the tile",
            "tile label text",
            "noop",
            GObject.PARAM_READWRITE),
        "hilite_tool": (
            Clutter.Actor.__gtype__,
            "actor to hilite", "hiliting tool",
            GObject.PARAM_READWRITE),
        "ratio_spacing": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.hilite_tool = None
        self._init_box()
        self._init_preview()
        self._init_label()

    @property
    def label_text(self):
        return self._label_text

    @label_text.setter
    def label_text(self, value):
        self._label_text = value
        self.label.set_text(value)

    @property
    def preview_path(self):
        return self._preview_path

    @preview_path.setter
    def preview_path(self, value):
        self._preview_path = value
        self.preview.set_from_file(value)

    @property
    def ratio_spacing(self):
        return self.box.ratio_spacing

    @ratio_spacing.setter
    def ratio_spacing(self, value):
        self.box.ratio_spacing = value

    @property
    def hilite_tool(self):
        return self._hilite_tool

    @hilite_tool.setter
    def hilite_tool(self, value):
        self._hilite_tool = value

    def _init_box(self):
        self.box = layout.Box()
        self.box.orientation = Clutter.Orientation.VERTICAL
        self.add_child(self.box)

    def _init_preview(self):
        self.preview = Mx.Image()
        self.preview.set_scale_mode(Mx.ImageScaleMode.CROP)
        self.box.add_child(self.preview)

    def _init_label(self):
        self.label = Tile.Label()
        self.box.add_child(self.label)

    def hilite_off(self):
        # turn the hilite_tool off
        pass
        
    def hilite_on(self):
        # turn the hilite_tool on
        pass
