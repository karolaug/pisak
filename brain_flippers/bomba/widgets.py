'''
Widgets specific to Bomba game
'''
from gi.repository import Clutter
import time
import brain_flippers.widgets


class GraphicalCountdown(Clutter.Actor):
    __gtype_name__ = "BrainGraphicalCountdown"
    
    COUNTDOWN_IMAGES = [
        None, "bomba_01.jpg", "bomba_02.jpg", "bomba_03.jpg",
        "bomba_04.jpg", "bomba_05.jpg", "bomba_06.jpg", "bomba_07.jpg",
        "bomba_08.jpg", "bomba_09.jpg", "bomba_10.jpg"
    ]
    
    BUTTON_IMAGE = "bomba_guzik.jpg"
    
    
    def __init__(self):
        super().__init__()
    
    def start_countdown(self, hide_on):
        self._time_left = 10
        self._hide_on = hide_on
        self._interrupted = False
        self.show()
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
        else:
            image = self.COUNTDOWN_IMAGES[self._time_left]
        self._set_image(image)
        return True

    def _set_image(self, image):
        raise NotImplementedError()


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
