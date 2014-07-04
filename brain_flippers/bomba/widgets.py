'''
Widgets specific to Bomba game
'''
from gi.repository import Clutter, Mx, GObject
import time
import brain_flippers.widgets
import pisak.widgets
import random
from pisak import res


class GraphicalCountdown(Clutter.Actor):
    __gtype_name__ = "BrainGraphicalCountdown"

    COUNTDOWN_IMAGES = [
        None, "bomba/bomba_01.jpg", "bomba/bomba_02.jpg",
        "bomba/bomba_03.jpg", "bomba/bomba_04.jpg", "bomba/bomba_05.jpg",
        "bomba/bomba_06.jpg", "bomba/bomba_07.jpg", "bomba/bomba_08.jpg",
        "bomba/bomba_09.jpg", "bomba/bomba_10.jpg"
    ]

    BUTTON_IMAGE = "bomba/bomba_guzik.jpg"

    def __init__(self):
        super().__init__()

        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

        self.image = Mx.Image()
        self.add_child(self.image)

    def start_countdown(self, hide_on):
        self._time_left = 10
        self._hide_on = hide_on
        self._interrupted = False
        self.show()
        self._set_image(self.COUNTDOWN_IMAGES[self._time_left])
        self.start_time = time.time()
        Clutter.threads_add_timeout(0, 1000, self._tick, None)

    def hide(self):
        self.hide()
        self.interrupted = True

    def _tick(self, data):
        self._time_left -= 1
        if self._interrupted:
            return False
        if self._time_left == 0:
            return False
        if self._time_left == self._hide_on:
            image = self.BUTTON_IMAGE
            self._set_image(image)
            return False
        else:
            image = self.COUNTDOWN_IMAGES[self._time_left]
            self._set_image(image)
            return True

    def _set_image(self, image):
        path = res.get(image)
        self.image.set_from_file(path)


class TimingFeedback(brain_flippers.widgets.TextFeedback):
    __gtype_name__ = "BrainTimingFeedback"

    SUCCESS_MESSAGE = "Udało Ci się rozbroić bombę"
    FAILURE_MESSAGE = "Niestety, buchnąłeś bombę" 

    def __init__(self):
        super().__init__()

    def success(self, time_difference):
        self.show_feedback(self.FAILURE_MESSAGE, time_difference)

    def failrue(self, time_difference):
        self.show_feedback(self.FAILURE_MESSAGE, time_difference)

    def show_feedback(self, message, time_difference):
        self.text = message + "\n" + str(time_difference)
        self.show()


class Status(Clutter.Actor):
    __gtype_name__ = "BrainBombaStatus"

    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_elements()

    def _init_layout(self):
        self.layout = Clutter.BoxLayout()
        self.set_layout_manager(self.layout)

    def _init_elements(self):
        self.score_display = Mx.Label()
        self.add_child(self.score_display)

        self.lives_display = Mx.Label()
        self.add_child(self.lives_display)

        self.exit_button = Mx.Button.new_with_label("Wyjście")
        self.add_child(self.exit_button)

    def update_status(self, score, lives):
        score_text = "PUNKTY: {}".format(score)
        self.score_display.set_text(score_text)

        lives_text = "♥" * lives
        self.lives_display.set_text(lives_text)


class Logic(Clutter.Actor, pisak.widgets.PropertyAdapter):
    __gtype_name__ = "BrainBombaLogic" 

    __gsignals__ = {}

    __gproperties__ = {
        "status": (Status.__gtype__, "", "", GObject.PARAM_READWRITE),
        "countdown": (GraphicalCountdown.__gtype__, "", "",
            GObject.PARAM_READWRITE),
        "feedback": (
            brain_flippers.widgets.Dismissable.__gtype__, "", "",
            GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.set_fixed_position_set(True)

        self.score = 0
        self.lives = 3

        self.connect("notify::mapped", self._ready)

    def _ready(self, *args):
        self._initialize_game()

    def _initialize_game(self):
        self._start_round()

    def _start_round(self):
        self.hide_on = random.choice([8, 7, 6, 5, 4, 3, 2])
        self.countdown.start_countdown(self.hide_on)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        value.update_status(self.score, self.lives)

    @property
    def countdown(self):
        return self._countdown

    @countdown.setter
    def countdown(self, value):
        self._countdown = value

    @property
    def feedback(self):
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        self._feedback = value
