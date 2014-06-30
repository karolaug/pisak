import sys

from gi.repository import Clutter, Mx, Cogl, GObject
from PIL import Image

from pisak import switcher_app
from brain_flippers.puzzle.photo import Photo
from random import Random, choice
import os.path 
from os import getenv

class PuzzleBoard(Clutter.Actor):
    __gtype_name__ = "BrainPuzzleBoard"
    __gsignals__ = {
        "game_end": (GObject.SIGNAL_RUN_FIRST, None, ()),
        "game_over": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }
    
    BASE_PATH = os.path.split(__file__)[0]
    SCRIPT_PATH = os.path.join(BASE_PATH, "stage.json")
    IMAGES_PATH = os.path.join(getenv('HOME'), 'Pictures')
    try:
        IMAGES = [image for image in os.listdir(IMAGES_PATH) if os.path.splitext(image)[-1] == '.jpg']
        BASE_PATH = IMAGES_PATH
    except FileNotFoundError:
        print('It appears you do not have such a directory: {}'.format(IMAGES_PATH))
        IMAGES = ["paisaje-wallpaper-1920x1080.jpg"]
    PLAYER_LIFE_UNICHAR = u"\u2764"
    NR_PARTS = [4, 9, 16, 25, 36, 100]

    def __init__(self):
        super().__init__()
        self.player_points = 0
        self.player_errors = 0
        self.player_clock = 0
        self.player_score = 0
        self.player_lives = 4
        self.player_lives_left = self.player_lives
        self.player_clock_ticking = False
        self.player_clock_str = "00:00"
        self.one_second = 1000
        self.level = 0
        self.final_delay = 100
        self._load_script(self.level)

    def _load_script(self, level):
        if self.get_children():
            self.remove_all_children()
        self.randomizer = Random()
        Mx.Button() # workaround for GI loader
        self.script = Clutter.Script()
        self.script.load_from_file(self.SCRIPT_PATH)
        self.view_actor = self.script.get_object("main")
        self.image = self.script.get_object("image")
        self.photo = Photo(os.path.join(self.BASE_PATH, choice(self.IMAGES)))
        self.photo.rect_div(self.NR_PARTS[level%len(self.NR_PARTS)])
        self.photo.next_square()
        self.buttons = [self.script.get_object("button{}".format(i)) 
                        for i in range(1, 5)]
        for i in self.buttons:
            i.connect("clicked", self.next_frame)
        self.set_image_from_data()
        self.set_buttons_from_data()
        self.set_layout_manager(Clutter.BoxLayout())
        self.add_child(self.view_actor)
        self._display_player_clock()
        self._display_player_life_panel()
        self._display_level_info()
        self.player_clock_ticking = True
        Clutter.threads_add_timeout(0, self.one_second, self.update_player_clock, None)

    def _display_player_clock(self):
        self.script.get_object("clock").set_text(self.player_clock_str)

    def _display_player_life_panel(self):
        life_panel = self.script.get_object("life_panel")
        for life in range(self.player_lives_left):
            life_panel.insert_unichar(self.PLAYER_LIFE_UNICHAR)

    def _display_level_info(self):
        self.script.get_object("level_value").set_text(str(self.level+1) + " / " + str(len(self.NR_PARTS)))

    def on_life_loss(self):
        life_panel = self.script.get_object("life_panel")
        self.player_lives_left -= 1
        life_panel.set_text(life_panel.get_text()[:-1])
        if not self.player_lives_left:
            self.player_clock_ticking = False
            Clutter.threads_add_timeout(0, self.final_delay, self.end_game, None)
            
    def set_image_from_data(self):
        data = self.photo.unshaded.tostring()
        (width, height) = self.photo.image.size
        row_stride = len(data) / height
        self.image.set_from_data(data, Cogl.PixelFormat.RGB_888, width, 
                                 height, row_stride)

    def set_buttons_from_data(self):
        margin = Clutter.Margin.new()
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
            print(width, height)
            row_stride = len(data) / height
            img.set_scale_mode(1)
            img.set_from_data(data, Cogl.PixelFormat.RGB_888, width, height,
                              row_stride)
            button.status = part_photo[1]
            

    def next_frame(self, button):
        if button.status:
            self.player_points += 1
            if not self.photo.next_square():
                for button in self.buttons:
                    button.disconnect_by_func(self.next_frame)
                self.player_clock_ticking = False
                Clutter.threads_add_timeout(0, self.final_delay, self.next_level, None)
            else:
                self.set_image_from_data()
                self.set_buttons_from_data()
        else:
            self.player_errors += 1
            self.on_life_loss()

    def next_level(self, *args):
        self.level += 1
        if self.level < len(self.NR_PARTS):
            self._load_script(self.level)
        else:
            self.end_game()
        return False

    def end_game(self, *args):
        self.calculate_player_score()
        self.emit("game_end")

    def calculate_player_score(self):
        limit = 300
        error_coeff = 10
        level_coeff = self.player_clock + limit/5
        formula = limit - self.player_clock - error_coeff*self.player_errors + level_coeff*self.level
        self.player_score = round(formula, 2)

    def update_player_clock(self, source):
        if self.player_clock_ticking:
            self.player_clock += 1
            minutes = str(self.player_clock//60)
            seconds = str(self.player_clock%60)
            minutes = (2-len(minutes)) * "0" + minutes
            seconds = (2-len(seconds)) * "0" + seconds
            self.player_clock_str = minutes+":"+seconds
            self.script.get_object("clock").set_text(self.player_clock_str)
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
