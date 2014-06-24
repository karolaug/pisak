from gi.repository import Clutter, cairo, GObject, Mx

class PuzzleButton(Clutter.Actor):
    __gtype_name__ = "BrainPuzzleButton"
    __gsignals__ = {
        "activate": (
            GObject.SIGNAL_RUN_FIRST,
            None,
            ())
    }
    __gproperties__ = {
         "label": (
             GObject.TYPE_STRING,
             "label on the key",
             "label displayed on the key",
             "",
             GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.r, self.g, self.b, self.a = 0, 0.1, 0.2, 0.5
        self.label_font = "Sans 20"
        self.hilite_duration = 1000
        self.set_layout_manager(Clutter.BinLayout())
        self._init_canvas()
        self._init_label_entry()
        self.set_reactive(True)
        self.connect("button-press-event", self.event_activate)
        self.connect("touch-event", self.event_activate)

    def _init_canvas(self):
        canvas = Clutter.Canvas()
        canvas.connect("draw", self.update_canvas)
        canvas.set_size(20, 20)
        canvas.invalidate()
        self.set_content(canvas)

    def _init_label_entry(self):
        self.label_entry = Clutter.Text()
        color = Clutter.Color.new(self.r*255, self.g*255, self.b*255, 255)
        self.label_entry.set_color(color)
        self.label_entry.set_font_name(self.label_font)
        self.add_child(self.label_entry)

    def update_canvas(self, canvas, context, w, h):
        context.scale(w, h)
        context.set_line_width(0.2)
        context.move_to(0, 0)
        context.line_to(1, 0)
        context.line_to(1, 1)
        context.line_to(0, 1)
        context.line_to(0, 0)
        context.set_source_rgba(self.r, self.g, self.b, self.a)
        context.stroke()
        return True

    def update_label(self):
        self.label_entry.set_text(self.label)

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.update_label()

    def do_set_property(self, spec, value):
        """
        Introspect object properties and set the value.
        """
        attribute = self.__class__.__dict__.get(spec.name.replace("-", "_"))
        if attribute is not None and isinstance(attribute, property):
            attribute.fset(self, value)
        else:
            raise ValueError("No such property", spec.name.replace("-", "_"))

    def do_get_property(self, spec):
        """
        Introspect object properties and get the value.
        """
        attribute = self.__class__.__dict__.get(spec.name.replace("-", "_"))
        if attribute is not None and isinstance(attribute, property):
            return attribute.fget(self)
        else:
            raise ValueError("No such property", spec.name.replace("-", "_"))

    def event_activate(self, source, event):
        if isinstance(event, Clutter.TouchEvent):
            if event.type != 13:  # touch-begin type of event
                return None
        self.emit("activate")
        self.hilite_on()

    def hilite_on(self):
        effect = Clutter.BlurEffect.new()
        self.add_effect_with_name("hilite", effect)
        Clutter.threads_add_timeout(0, self.hilite_duration, self.hilite_off, None)

    def hilite_off(self, data):
        self.remove_effect_by_name("hilite")


class ScoreSummary(Clutter.Actor):
    """
    Actor which allow displaying unified score summaries
    """
    __gtype_name__ = "BrainScoreSummary"
    
    __gsignals__ = {}
    
    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_elements()
    
    def _init_layout(self):
        self.layout = Clutter.GridLayout()
        self.set_layout_manager()
    
    def _init_elements(self):
        self.dismiss_button = Mx.Button()
        self.dismiss_button.set_label(">")
    
    def display_score(self, entries, old_score):
        """
        Show the actor with supplied level score summary
        """
        for row, (description, score) in enumerate(entries):
            description_label = Mx.Label.new_with_text(description)
            score_label = Mx.Label.new_with_text(str(score))
            self.layout.attach(description_label, row, 0, 1, 1)
            self.layout.attach(score_label, row, 1, 1, 1)
        self.layout.attach(self.dismiss_button, len(entries), 0, 2, 1)
        self.show()
       