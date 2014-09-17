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

    BOMBA_IMAGE = "bomba/bomba.jpg"

    TIME = 10

    def __init__(self):
        super().__init__()

        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

        self.image = Mx.Image()
        self.add_child(self.image)
        self.button = Button()
        self.button.set_size(200, 200)
        self.button.set_position(800, 500)
        self.add_child(self.button)

    def start_countdown(self, hide_on):
        self._time_left = self.TIME
        self._hide_on = hide_on
        self._interrupted = False
        self._set_image(self.COUNTDOWN_IMAGES[self._time_left])
        self.start_time = time.time()
        Clutter.threads_add_timeout(0, 1000, self._tick, None)

    def _tick(self, data):
        self._time_left -= 1
        if self._interrupted:
            return False
        if self._time_left == 0:
            return False
        if self._time_left <= self._hide_on:
            image = self.BOMBA_IMAGE
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

    SUCCESS_MESSAGE = "BRAWO!!!\nUdało Ci się rozbroić bombę!\n"
    FAILURE_MESSAGE = "Niestety, w złym momencie\nzatrzymałeś licznik!\n" 

    def __init__(self):
        super().__init__()

    def success(self, time_difference):
        self.show_feedback(self.SUCCESS_MESSAGE, time_difference)

    def failure(self, time_difference, custom_feedback=False):
        if custom_feedback:
            self.FAILURE_MESSAGE = custom_feedback
        self.show_feedback(self.FAILURE_MESSAGE, time_difference)

    def show_feedback(self, message, time_difference):
        self.text = message + "\nUpłyneło " + str(time_difference) + "sek. od włączenia zegara."
        self.show()


class VideoFeedback(brain_flippers.widgets.VideoFeedback):
    __gtype_name__ = "BrainMalpaVideo"

    def __init__(self):
        super().__init__()

    def play(self):
        self.video_texture.set_playing(True)

class Button(Mx.Button):
    __gtype_name__ = "BrainBombaButton"

    def __init__(self):
        super().__init__()


class Status(Clutter.Actor):
    __gtype_name__ = "BrainBombaStatus"

    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_elements()

    def _init_layout(self):
        self.layout = Clutter.BoxLayout()
        self.layout.set_spacing(100)
        self.set_layout_manager(self.layout)

    def _init_elements(self):
        self.score_display = brain_flippers.widgets.FeedbackLabel()
        self.add_child(self.score_display)

        self.lives_display = brain_flippers.widgets.FeedbackLabel()
        self.add_child(self.lives_display)

        #self.exit_button = Mx.Button.new_with_label("Wyjście")
        #self.add_child(self.exit_button)

    def update_status(self, score, lives):
        score_text = "PUNKTY: {} ".format(score)
        self.score_display.set_text(score_text)

        lives_text = "Życie: " + "♥" * lives
        self.lives_display.set_text(lives_text)

class Logic(Clutter.Actor, pisak.widgets.PropertyAdapter):
    __gtype_name__ = "BrainBombaLogic" 

    __gsignals__ = {
        "finished": (GObject.SIGNAL_RUN_FIRST, None, [])}

    __gproperties__ = {
        "status": (Status.__gtype__, "", "", GObject.PARAM_READWRITE),
        "countdown": (GraphicalCountdown.__gtype__, "", "",
            GObject.PARAM_READWRITE),
        "feedback": (
            brain_flippers.widgets.Dismissable.__gtype__, "", "",
            GObject.PARAM_READWRITE),
        "video_feedback": (
            VideoFeedback.__gtype__, "", "", GObject.PARAM_READWRITE)
    }

    def __init__(self):
        super().__init__()
        self.set_fixed_position_set(True)

        self.score = 0
        self.lives = 3
        self.successes = 0

        self.connect("notify::mapped", self._ready)

    def _ready(self, *args):
        self._initialize_game()

    def _initialize_game(self):
        self._start_round()
    
    def _start_round(self):
        self.video_feedback.dismiss()
        self.countdown.image.show()
        self.hide_on = random.choice([8, 7, 6, 5, 4, 3, 2])
        self.countdown.start_countdown(self.hide_on)

    def interrupt(self, button):
        self.countdown._interrupted = True
        self.elpased = round(time.time() - self.countdown.start_time)
        self.countdown.image.hide()
        if self.elpased == self.countdown.TIME:
            self.success()
        else:
            self.failure()
        self.status.update_status(self.score, self.lives)

    def success(self):
        self.score += self.hide_on * 10
        self.successes += 1
        self.feedback.success(round(time.time() - self.countdown.start_time, 1))
        
    def failure(self):
        self.lives -= 1
        if self.lives == 0:
            self.feedback.failure(round(time.time() - self.countdown.start_time, 1), custom_feedback="\nNiestety wykorzystales juz wszystkie zycia!\nZostaniesz, przeniesiony do ekranu\nkońcowego.\n")
        else:
            self.feedback.failure(round(time.time() - self.countdown.start_time, 1))
        self.video_feedback.show()
        self.video_feedback.play()

    def what_next(self, *args):
        if self.lives == 0:
            self.video_feedback.video_texture.set_playing(False)
            self.video_feedback.unparent()
            self.countdown.unparent()
            self.end_game()
        else:
            self._start_round()

    def end_game(self, *args):
        self.emit("finished")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        value.update_status(self.score, self.lives)
        #value.exit_button.connect("clicked", self.end_game)

    @property
    def countdown(self):
        return self._countdown

    @countdown.setter
    def countdown(self, value):
        value.button.connect("clicked", self.interrupt)
        self._countdown = value

    @property
    def feedback(self):
        return self._feedback

    @feedback.setter
    def feedback(self, value):
        self._feedback = value
        value.dismiss_button.connect("clicked", self.what_next)

    @property
    def video_feedback(self):
        return self._video_feedback

    @video_feedback.setter
    def video_feedback(self, value):
        self._video_feedback = value
