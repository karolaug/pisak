import sys

from gi.repository import Clutter, Mx, Cogl
from PIL import Image

from pisak import switcher_app
from brain_flippers.puzzles.photo import Photo
from random import Random

class PuzzleStage(Clutter.Stage):
    SCRIPT_PATH = "stage.json"

    def __init__(self, context):
        super().__init__()
        self.context = context
        self._load_script()

    def _load_script(self):
        self.randomizer = Random()
        Mx.Button() # workaround for GI loader
        self.script = Clutter.Script()
        self.script.load_from_file(self.SCRIPT_PATH)
        self.view_actor = self.script.get_object("main")
        self.image = self.script.get_object("image")
        self.photo = Photo('paisaje-wallpaper-1920x1080.jpg')
        self.photo.next_square()
        self.buttons = [self.script.get_object("button{}".format(i)) 
                        for i in range(1,5)]
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

class PuzzleApp(switcher_app.Application):
    """
    Brain flipper app with brain flipper stage.
    """
    def create_stage(self, argv):
        stage = PuzzleStage(self.context)
        stage.set_fullscreen(True)
        return stage


if __name__ == "__main__":
    PuzzleApp(sys.argv).main()
