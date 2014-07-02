from gi.repository import Clutter, GObject, Mx, Gst, ClutterGst
from pisak.widgets import PropertyAdapter

from pisak.widgets import PropertyAdapter

class PuzzleButton(Clutter.Actor, PropertyAdapter):
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
             GObject.PARAM_READWRITE),
         "label_font": (
             GObject.TYPE_STRING,
             "font of the label",
             "font name of the label",
             "",
             GObject.PARAM_READWRITE),
    }

    def __init__(self):
        super().__init__()
        self.r, self.g, self.b, self.a = 0.21, 0.69, 0.87, 1
        self._init_label_entry()
        self.label_font = "Sans 20"
        self.hilite_duration = 1000
        self.set_layout_manager(Clutter.BinLayout())
        self._init_canvas()
        self.set_reactive(True)
        self.connect("button-press-event", self.fire_activate)
        self.connect("touch-event", self.fire_activate)

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

    def set_label(self, value):
        self.label = value

    def get_label(self):
        return self.label

    def set_label_font(self, value):
        self.label_font = value

    def get_label_font(self):
        return self.label_font

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        self._label = value
        self.label_entry.set_text(self.label)

    @property
    def label_font(self):
        return self._label_font

    @label_font.setter
    def label_font(self, value):
        self._label_font = value
        self.label_entry.set_font_name(self.label_font)

    def fire_activate(self, source, event):
        if isinstance(event, Clutter.TouchEvent):
            if event.type != 13:  # touch-begin type of event
                return None
        self.emit("activate")
        self.hilite_on()

    def hilite_on(self):
        if not self.get_effect("hilite"):
            effect = Clutter.BlurEffect.new()
            self.add_effect_with_name("hilite", effect)
            Clutter.threads_add_timeout(0, self.hilite_duration, self.hilite_off, None)

    def hilite_off(self, *args):
        self.remove_effect_by_name("hilite")


class Dismissable(Clutter.Actor):
    __gsignals__ = {
        "dismissed": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        super().__init__()

    def dismiss(self, *args):
        self.hide()
        self.emit("dismissed")


class ScoreSummary(Dismissable):
    """
    Actor which allow displaying unified score summaries
    """
    __gtype_name__ = "BrainScoreSummary"

    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_elements()

    def _init_layout(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

    def _init_elements(self):
        self.dismiss_button = Mx.Button()
        self.dismiss_button.set_label(">")
        self.dismiss_button.connect("clicked", self.dismiss)
        self.grid = Clutter.Actor()
        self.grid_layout = Clutter.GridLayout()
        self.grid.set_layout_manager(self.grid_layout)
        self.add_child(self.grid)

    def dismiss(self, *args):
        super().dismiss(*args)
        self.grid.remove_all_children()

    def display_score(self, entries, total_score):
        """
        Show the actor with supplied level score summary
        """
        row = 0
        score_sum = 0
        for description, score in entries:
            description_label = Mx.Label.new_with_text(description)
            score_label = Mx.Label.new_with_text(str(score))
            self.grid_layout.attach(description_label, 0, row, 1, 1)
            self.grid_layout.attach(score_label, 1, row, 1, 1)
            score_sum += score
            row += 1
        round_label = Mx.Label.new_with_text("suma punktów za rundę")
        round_score_label = Mx.Label.new_with_text(str(score_sum))
        total_label = Mx.Label.new_with_text("aktualny wynik")
        total_score_label = Mx.Label.new_with_text(str(total_score))
        self.grid_layout.attach(round_label, 0, row + 2, 1, 1)
        self.grid_layout.attach(round_score_label, 1, row + 2, 1, 1)
        self.grid_layout.attach(total_label, 0, row + 4, 1, 1)
        self.grid_layout.attach(total_score_label, 1, row + 4, 1, 1)
        self.grid_layout.attach(self.dismiss_button, 0, row + 6, 2, 1)
        self.show()


class TextFeedback(Dismissable, PropertyAdapter):
    __gtype_name__ = "BrainTextFeedback"

    __gproperties__ = {
        "text": (GObject.TYPE_STRING, "", "", "", GObject.PARAM_READWRITE),
        "color": (Clutter.Color.__gtype__, "", "", GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

        self.box = Clutter.Actor()
        self.box.set_layout_manager(Clutter.BoxLayout())
        self.add_actor(self.box)

        self.label = Mx.Label()
        self.box.add_actor(self.label)

        self.dismiss_button = Mx.Button.new_with_label(">")
        self.dismiss_button.connect("clicked", self.dismiss)
        self.box.add_actor(self.dismiss_button)

    def display(self):
        self.show()

    @property
    def text(self):
        return self.label.get_text()

    @text.setter
    def text(self, value):
        self.label.set_text(value)

    @property
    def color(self):
        return self.label.get_clutter_text().get_color()

    @color.setter
    def color(self, value):
        self.label.get_clutter_text().set_color(value)


class VideoFeedback(Clutter.Actor):
    __gtype_name__ = "BrainVideoFeedback"

    __gsignals__ = {    
        "dismissed": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        ClutterGst.init()
        self.video_texture = ClutterGst.VideoTexture(**{"disable-slicing": True})
        #self.video_texture.set_x_expand(True)
        #self.video_texture.set_y_expand(True)
        self.add_child(self.video_texture)

        descriptor = "playbin uri=http://docs.gstreamer.com/media/sintel_trailer-480p.webm"
        self.pipeline = Gst.parse_launch(descriptor)

        self.clutter_sink = Gst.ElementFactory.make("autocluttersink")
        self.clutter_sink.set_property("texture", self.video_texture)
        self.pipeline.set_property("video-sink", self.clutter_sink)

        self.pipeline.set_state(Gst.State.PLAYING)
