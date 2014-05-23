'''
Definitions of classes built-in with layout managers . These actors can
be used to describe whole application view in ClutterScript. Relevant
layout parameters are proxied to internal layout manager.
'''
from gi.repository import Clutter, GObject


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
        "spacing": (
            GObject.TYPE_UINT,
            "", "",
            0, GObject.G_MAXUINT, 0,
            GObject.PARAM_READWRITE),
    }
    
    def __init__(self):
        super().__init__()
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)
    
    def do_get_property(self, spec):
        return self.layout.get_property(spec.name)
    
    def do_set_property(self, spec, value):
        self.layout.set_property(spec.name, value)
