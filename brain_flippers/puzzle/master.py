import sys

from gi.repository import Clutter, Mx, Cogl, GObject
from PIL import Image

from pisak import switcher_app
from brain_flippers.puzzle.photo import Photo
from random import Random
import os.path


class PuzzleBoard(Clutter.Actor):
    __gtype_name__ = "BrainPuzzleBoard"
    __gsignals__ = {
        "game_end": (GObject.SIGNAL_RUN_FIRST, None, ()),
        "game_over": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }
    
    BASE_PATH = os.path.split(__file__)[0]
    SCRIPT_PATH = os.path.join(BASE_PATH, "stage.json")
    IMAGE_PATH = os.path.join(BASE_PATH, "paisaje-wallpaper-1920x1080.jpg")

    def __init__(self):
        super().__init__()
        self.player_points = 0
        self.player_errors = 0
        self.player_clock = 0
        self.player_score = 0
        self.player_lives = 4
        self.player_clock_ticking = True
        self.final_delay = 2000
        self._load_script()
        self._display_player_clock()
        self._display_player_life_panel()
        one_second = 1000
        Clutter.threads_add_timeout(0, one_second, self.update_player_clock, None)

    def _load_script(self):
        self.randomizer = Random()
        Mx.Button() # workaround for GI loader
        self.script = Clutter.Script()
        self.script.load_from_file(self.SCRIPT_PATH)
        self.view_actor = self.script.get_object("main")
        self.image = self.script.get_object("image")
        self.photo = Photo(self.IMAGE_PATH)
        self.photo.next_square()
        self.buttons = [self.script.get_object("button{}".format(i)) 
                        for i in range(1, 5)]
        for i in self.buttons:
            i.connect("clicked", self.next_frame)
        self.set_image_from_data()
        self.set_buttons_from_data()
        self.set_layout_manager(Clutter.BoxLayout())
        self.add_child(self.view_actor)

    def _display_player_clock(self):
        self.script.get_object("clock").set_text("00:00")

    def _display_player_life_panel(self):
        life_panel = self.script.get_object("life_panel")
        life_panel.set_text(self.player_lives*"+ ")

    def on_life_loss(self):
        life_panel = self.script.get_object("life_panel")
        life_panel.set_text(life_panel.get_text()[:-2])
        if not life_panel.get_text():
            self.emit("game_over")
            
    def set_image_from_data(self):
        data = self.photo.unshaded.tostring()
        (width, height) = self.photo.image.size
        row_stride = len(data) / height
        self.image.set_from_data(data, Cogl.PixelFormat.RGB_888, width, 
                                 height, row_stride)

    def set_buttons_from_data(self):
        mirror = Image.FLIP_LEFT_RIGHT
        rotation_fakes = [0, 90, 180, 270]
        rotation_right = [90, 180, 270]
        cropped = self.photo.part_image
        fakes = [cropped.transpose(mirror) for i in range(3)]
        self.randomizer.shuffle(rotation_fakes)
        fakes = [(i.rotate(rotation_fakes.pop()), False) for i in fakes]
        right = (cropped.rotate(self.randomizer.choice(rotation_right)), True)
        fakes.append(right)
        self.randomizer.shuffle(fakes)
        for button, part_photo in zip(self.buttons, fakes):
            img = [i for i in button.get_children() if type(i) == Mx.Image][0]
            data = part_photo[0].tostring()
            (width, height) = part_photo[0].size
            row_stride = len(data) / height
            img.set_from_data(data, Cogl.PixelFormat.RGB_888, width, height,
                              row_stride)
            button.status = part_photo[1]

    def next_frame(self, button):
        if button.status:
            self.player_points += 1
            if not self.photo.next_square():
                for button in self.buttons:
                    button.disconnect_by_func(self.next_frame)
                Clutter.threads_add_timeout(0, self.final_delay, self.end_game, None)
            else:
                self.set_image_from_data()
                self.set_buttons_from_data()
        else:
            self.player_errors += 1
            self.on_life_loss()

    def end_game(self, *args):
        self.player_clock_ticking = False
        self.calculate_player_score()
        self.emit("game_end")
        return False

    def calculate_player_score(self):
        limit = 300
        coeff = 10
        formula = limit - self.player_clock/len(self.photo.parts) - coeff*(self.player_errors - len(self.photo.parts)/2)
        self.player_score = round(formula, 2)

    def update_player_clock(self, source):
        if self.player_clock_ticking:
            self.player_clock += 1
            minutes = str(self.player_clock//60)
            seconds = str(self.player_clock%60)
            minutes = (2-len(minutes)) * "0" + minutes
            seconds = (2-len(seconds)) * "0" + seconds
            self.script.get_object("clock").set_text(minutes+":"+seconds)
            return True
        else: 
            return False


class Logic(GObject.GObject):
    __gtype_name__ = "BrainPuzzleLogic"
    __gproperties__ = {
        "board": (PuzzleBoard.__gtype__, "", "", GObject.PARAM_READWRITE),
        #"status_bar": (PuzzleStatus.__gtype__, "", "", GObject.PARAM_READWRITE),
        "answer_1": (Mx.Button.__gtype__, "", "", GObject.PARAM_READWRITE),
        "answer_2": (Mx.Button.__gtype__, "", "", GObject.PARAM_READWRITE),
        "answer_3": (Mx.Button.__gtype__, "", "", GObject.PARAM_READWRITE),
        "answer_4": (Mx.Button.__gtype__, "", "", GObject.PARAM_READWRITE),
    }
