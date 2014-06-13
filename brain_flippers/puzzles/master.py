import sys

from gi.repository import Clutter, Mx, Cogl
from PIL import Image

from pisak import switcher_app
from brain_flippers.puzzles.photo import Photo
from random import Random
import os.path

class PuzzleBoard(Clutter.Actor):
    __gtype_name__ = "BrainPuzzleBoard"
    
    BASE_PATH = os.path.split(__file__)[0]
    SCRIPT_PATH = os.path.join(BASE_PATH, "stage.json")
    IMAGE_PATH = os.path.join(BASE_PATH, "paisaje-wallpaper-1920x1080.jpg")

    def __init__(self):
        super().__init__()
        self._load_script()

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
        self.buttons[0].connect("clicked", self.next_frame)
        self.set_image_from_data()
        self.set_buttons_from_data()
        self.set_layout_manager(Clutter.BoxLayout())
        self.add_child(self.view_actor)

    def set_image_from_data(self):
        data = self.photo.unshaded.tostring()
        (width, height) = self.photo.image.size
        row_stride = len(data) / height
        self.image.set_from_data(data, Cogl.PixelFormat.RGB_888, width, 
                                 height, row_stride)

    def set_buttons_from_data(self):
        mirror = [Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM]
        rotation = [90, 270, 180]
        cropped = self.photo.part_image
        fakes = [cropped.transpose(self.randomizer.choice(mirror)) 
                 for _ in range(3)]
        fakes = [(i.rotate(self.randomizer.choice(rotation[:2])), False) 
                 for i in fakes]
        right = (cropped.rotate(self.randomizer.choice(rotation)), True)
        fakes.append(right)
        self.randomizer.shuffle(fakes)
        for button, part_photo in zip(self.buttons, fakes):
            img = button.get_children()[0]
            data = part_photo[0].tostring()
            (width, height) = part_photo[0].size
            row_stride = len(data) / height
            img.set_from_data(data, Cogl.PixelFormat.RGB_888, width, height,
                              row_stride)

    def next_frame(self, event):
        self.photo.next_square()
        self.set_image_from_data()
        self.set_buttons_from_data()
