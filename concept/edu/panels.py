from gi.repository import Clutter
from pisak import buttons

class Panel(Clutter.Actor):
    def __init__(self, container):
        super().__init__()
        self.container = container
        layout = Clutter.BinLayout()
        self.set_layout_manager(layout)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.set_reactive(True)
        self.connect('button_release_event', lambda x, y: self.exit_panel())
        self._init_elements()

    def _init_info(self):
        self.info = buttons.TextField()
        self.add_actor(self.info)

    def _init_elements(self):
        #to be overwritten by child
        pass

    def set_font(self, font_name):
        self.info.set_font(font_name)

    def set_info(self, info):
        self.info.set_text(info)

    def exit_panel(self):
        self.container.change_panel()


class RewardPanel(Panel):
    def __init__(self, container):
        super().__init__(container)

    def _init_elements(self):
        self._init_info()
        self._init_reward()

    def _init_reward(self):
        pass #self.reward = song/movie

    def run_reward(self, reward_file_path):
        pass #self.reward.play

class ResultInfoPanel(Panel):
    def __init__(self, container):
        super().__init__(container)

    def _init_elements(self):
        self._init_info()

class PisakEduStage(Clutter.Stage):
    def __init__(self, container):
        super().__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        color = Clutter.Color.new(100,170,190,255)
        self.set_background_color(color)
        self._init_elements(container)

    def _init_elements(self, container):
        self.contents = container()
        self.contents.connect('destroy', lambda _:self.exit_app())
        self.add_actor(self.contents)

    def exit_app(self):
        self.destroy()

class PisakEduApp(object):
    def __init__(self, container, argv):
        PisakEduApp.APP = self
        Clutter.init(argv)
        self.stage = PisakEduStage(container)
        self.stage.connect("destroy", lambda _: Clutter.main_quit())
        self.stage.set_fullscreen(True)
        self.stage.show_all()

    def main(self):
        Clutter.main()
