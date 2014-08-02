'''
Definitions of classes built-in with layout managers . These actors can
be used to describe whole application view in ClutterScript. Relevant
layout parameters are proxied to internal layout manager.
'''
from gi.repository import Clutter, GObject

from pisak import unit


class Box(Clutter.Actor):
    """
    Arranges children in single line using BoxLayout.
    """
    __gtype_name__ = "PisakBoxLayout"
    
    __gproperties__ = {
        "orientation": (
            Clutter.Orientation.__gtype__,
            "", "",
            "horizontal",
            GObject.PARAM_READWRITE),
        "homogeneous": (
            GObject.TYPE_BOOLEAN,
            "whether children should be homo",
            "children homogeneous", False,
            GObject.PARAM_READWRITE),
        "spacing": (
            GObject.TYPE_UINT,
            "", "",
            0, GObject.G_MAXUINT, 0,
            GObject.PARAM_READWRITE),
        "ratio_spacing": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_margin_bottom": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_margin_top": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_margin_right": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_margin_left": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
    }
    
    def __init__(self):
        super().__init__()
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)

    def _set_px_spacing(self, *args):
        if hasattr(self, "ratio_spacing"):
            if self.layout.get_orientation() == Clutter.Orientation.HORIZONTAL:
                px_spacing = unit.w(self.ratio_spacing)
            elif self.layout.get_orientation() == Clutter.Orientation.VERTICAL:
                px_spacing = unit.h(self.ratio_spacing)
            self.layout.set_spacing(px_spacing)
        
    @property
    def orientation(self):
        return self.layout.get_orientation()

    @orientation.setter
    def orientation(self, value):
        self.layout.set_orientation(value)
        self._set_px_spacing()

    @property
    def ratio_spacing(self):
        return self._ratio_spacing

    @ratio_spacing.setter
    def ratio_spacing(self, value):
        self._ratio_spacing = value
        self._set_px_spacing()

    @property
    def ratio_margin_bottom(self):
        return self._ratio_margin_bottom

    @ratio_margin_bottom.setter
    def ratio_margin_bottom(self, value):
        self._ratio_margin_bottom = value
        self.set_margin_bottom(unit.h(value))

    @property
    def ratio_margin_top(self):
        return self._ratio_margin_top

    @ratio_margin_top.setter
    def ratio_margin_top(self, value):
        self._ratio_margin_top = value
        self.set_margin_top(unit.h(value))

    @property
    def ratio_margin_right(self):
        return self._ratio_margin_right

    @ratio_margin_right.setter
    def ratio_margin_right(self, value):
        self._ratio_margin_right = value
        self.set_margin_right(unit.w(value))

    @property
    def ratio_margin_left(self):
        return self._ratio_margin_left

    @ratio_margin_left.setter
    def ratio_margin_left(self, value):
        self._ratio_margin_left = value
        self.set_margin_left(unit.w(value))
    
    def do_set_property(self, spec, value):
        """
        Introspect object properties and set the value.
        """
        attribute = self.__class__.__dict__.get(spec.name.replace("-", "_"))
        if attribute is not None and isinstance(attribute, property):
            attribute.fset(self, value)
        else:
            self.layout.set_property(spec.name, value)

    def do_get_property(self, spec):
        """
        Introspect object properties and get the value.
        """
        attribute = self.__class__.__dict__.get(spec.name.replace("-", "_"))
        if attribute is not None and isinstance(attribute, property):
            return attribute.fget(self)
        else:
            self.layout.get_property(spec.name)


class Bin(Clutter.Actor):
    __gtype_name__ = "PisakBinLayout"
    __gproperties__ = {
        "ratio_margin_bottom": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_margin_top": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_margin_right": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
        "ratio_margin_left": (
            GObject.TYPE_FLOAT,
            None, None, 0, 1., 0,
            GObject.PARAM_READWRITE),
    }
    
    def __init__(self):
        super().__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

    @property
    def ratio_margin_bottom(self):
        return self._ratio_margin_bottom

    @ratio_margin_bottom.setter
    def ratio_margin_bottom(self, value):
        self._ratio_margin_bottom = value
        self.set_margin_bottom(unit.h(value))

    @property
    def ratio_margin_top(self):
        return self._ratio_margin_top

    @ratio_margin_top.setter
    def ratio_margin_top(self, value):
        self._ratio_margin_top = value
        self.set_margin_top(unit.h(value))

    @property
    def ratio_margin_right(self):
        return self._ratio_margin_right

    @ratio_margin_right.setter
    def ratio_margin_right(self, value):
        self._ratio_margin_right = value
        self.set_margin_right(unit.w(value))

    @property
    def ratio_margin_left(self):
        return self._ratio_margin_left

    @ratio_margin_left.setter
    def ratio_margin_left(self, value):
        self._ratio_margin_left = value
        self.set_margin_left(unit.w(value))

    def do_set_property(self, spec, value):
        """
        Introspect object properties and set the value.
        """
        attribute = self.__class__.__dict__.get(spec.name.replace("-", "_"))
        if attribute is not None and isinstance(attribute, property):
            attribute.fset(self, value)
        else:
            self.layout.set_property(spec.name, value)

    def do_get_property(self, spec):
        """
        Introspect object properties and get the value.
        """
        attribute = self.__class__.__dict__.get(spec.name.replace("-", "_"))
        if attribute is not None and isinstance(attribute, property):
            return attribute.fget(self)
        else:
            self.layout.get_property(spec.name)
