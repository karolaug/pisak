from gi.repository import Clutter, GObject, Mx, Gst, ClutterGst
from pisak.widgets import PropertyAdapter
from brain_flippers import score_manager

class Consolation(Mx.Label):
    __gtype_name__ = "BrainConsolation"

    def __init__(self):
        super().__init__()

class TryAgain(Mx.Button):
    __gytpe_name__ = "BrainTryAgain"

    def __init__(self):
        super().__init__()

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

class DismissButton(Mx.Button):
    __gtype_name__ = "BrainDismissButton"

    def __init__(self):
        super().__init__()

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
        self.dismiss_button = DismissButton()
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

class FeedbackLabel(Mx.Label):
    __gtype_name__ = "BrainFeedbackLabel"

    def __init__(self):
        super().__init__()

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
        self.box_layout = Clutter.BoxLayout()
        self.box_layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.box.set_layout_manager(self.box_layout)
        self.add_actor(self.box)

        self.label = FeedbackLabel()
        self.box.add_actor(self.label)

        self.dismiss_button = DismissButton()
        self.dismiss_button.set_label("Spróbuj jeszcze raz!")
        self.dismiss_button.set_margin_top(200)
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


class VideoFeedback(Clutter.Actor, PropertyAdapter):
    __gtype_name__ = "BrainVideoFeedback"

    __gsignals__ = {    
        "dismissed": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    __gproperties__ = {
        "path": (GObject.TYPE_STRING, "", "", "", GObject.PARAM_READWRITE)}

    def __init__(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        ClutterGst.init()
        self.video_texture = ClutterGst.VideoTexture(**{"disable-slicing": 
                                                        True})
        self.add_child(self.video_texture)

    def dismiss(self):
        self.video_texture.set_playing(False)
        self.video_texture.set_progress(0.0)
        self.hide()

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
        self.video_texture.set_filename(value)


class TopResultLogic(Clutter.Actor, PropertyAdapter):
    __gtype_name__ = "BrainTopResultLogic"

    __gproperties__ = {
        "keyboard": (Clutter.Actor.__gtype__, "", "", GObject.PARAM_READWRITE),
        "player-score": (Clutter.Text.__gtype__, "", "", GObject.PARAM_READWRITE),
        "total-average-score": (Clutter.Text.__gtype__, "", "", GObject.PARAM_READWRITE),
        "player-name": (Clutter.Text.__gtype__, "", "", GObject.PARAM_READWRITE),
        "back-button": (Clutter.Actor.__gtype__, "", "", GObject.PARAM_READWRITE),
    }
    
    __gsignals__ = {
        "finished": (GObject.SIGNAL_RUN_FIRST, None, ()),
        "move-on": (GObject.SIGNAL_RUN_FIRST, None, ())
    }

    def __init__(self):
        super().__init__()
        self.set_fixed_position_set(True)
        self._keyboard = None
        self._player_score = None
        self._player_name = None
        self._total_average_score = None
        self._connected = False
        
        self.game_score = None
        self.typed_player_name = ""
        self.connect("notify::mapped", self._on_ready)

    def _on_ready(self, *args):
        if self.keyboard:
            self._connect_keyboard()

    @property
    def game_score(self):
        return self._game_score

    @game_score.setter
    def game_score(self, value):
        self._game_score = value
        if self.player_score:
            self._update_player_score()

    def _update_player_score(self):
        self.player_score.set_text(str(self.game_score))

    @property
    def game_name(self):
        return self._game_name

    @game_name.setter
    def game_name(self, value):
        self._game_name = value
        self._update_average_score()

    def _update_average_score(self):
        if self.total_average_score:
            game_average = score_manager.get_average_ever(self.game_name)
            if game_average:
                self.total_average_score.set_text(str(int(game_average)))
            else:
                self.total_average_score.set_text("brak wyników")
    
    @property
    def typed_player_name(self):
        return self._typed_player_name
    
    @typed_player_name.setter
    def typed_player_name(self, value):
        self._typed_player_name = value
        if self.player_name:
            self._update_player_name()
    
    def _update_player_name(self):
        if self.typed_player_name == "":
            self.player_name.set_text("_ _")
        elif len(self.typed_player_name) == 1:
            self.player_name.set_text(self.typed_player_name + " _")
        else:
            name = self.typed_player_name
            self.player_name.set_text("{} {}".format(name[0], name[1]))
            score_manager.add_record(
                self.game_name, self.typed_player_name, self.game_score)
            self.emit("move-on")
            

    # GObject properties

    @property
    def keyboard(self):
        return self._keyboard

    @keyboard.setter
    def keyboard(self, value):
        self._keyboard = value
    
    def _connect_keyboard(self):
        if self._connected:
            return
        self._connected = True
        to_scan = [self.keyboard]
        while (len(to_scan) > 0):
            current = to_scan.pop()
            if isinstance(current, PuzzleButton):
                current.connect("activate", self._type_letter)
            else:
                to_scan.extend(current.get_children())
                
    
    def _type_letter(self, source):
        if len(self.typed_player_name) < 2:
            self.typed_player_name = self.typed_player_name + source.get_label()

    @property
    def player_score(self):
        return self._player_score

    @player_score.setter
    def player_score(self, value):
        self._player_score = value
        self._update_player_score()

    @property
    def total_average_score(self):
        return self._total_average_score

    @total_average_score.setter
    def total_average_score(self, value):
        self._total_average_score = value

    @property
    def player_name(self):
        return self._player_name

    @player_name.setter
    def player_name(self, value):
        self._player_name = value
        self._update_player_name()

    @property
    def back_button(self):
        return self._back_button

    @back_button.setter
    def back_button(self, value):
        self._back_button = value
        value.connect("activate", self._finish)

    def _finish(self, *args):
        self.emit("finished")


class TopResultsListLogic(Clutter.Actor, PropertyAdapter):
    __gtype_name__ = "BrainTRLLogic"

    __gproperties___ = {
        "results-table": (Clutter.Actor.__gtype__, "", "", GObject.PARAM_READWRITE),
        "best-score": (Clutter.Text.__gtype__, "", "", GObject.PARAM_READWRITE),
        "game": (GObject.TYPE_STRING, "", "", "", GObject.PARAM_READWRITE),
        "only-today": (GObject.TYPE_BOOLEAN, "", "", False, GObject.PARAM_READWRITE),
    }

    def __init__(self):
        super().__init__()
        self.layout = Clutter.GridLayout()
        self.set_layout_manager(self.layout)
        self._results_table = None
        self._game = None
        self._only_today = True
        self._best_score = None

    @property
    def game(self):
        return self._game

    @game.setter
    def game(self, value):
        self._game = value

    @property
    def only_today(self):
        return self._only_today

    @only_today.setter
    def only_today(self, value):
        self._only_today = value

    @property
    def results_table(self):
        return self._results_table

    @results_table.setter
    def results_table(self, value):
        self._results_table = value

    @property
    def best_score(self):
        return self._best_score

    @best_score.setter
    def best_score(self, value):
        self._best_score = value
    
    def generate_results(self):
        """
        Query results based on widget settings. It must be called to display
        results.
        """
        if self.only_today:
            results = score_manager.get_best_today(self.game)
        else:
            results = scoe_manager.get_best_ever(self.game)
        best_score = str(results[0][1])
        self.best_score.set_text(best_score)
        for idx, row in enumerate(self.results_table.get_children()):
            if idx < len(results):
                fields = row.get_children()
                fields[1].set_text(results[idx][0])
                fields[2].set_text(str(results[idx][1]))
            else:
                row.hide()
            
        
            
