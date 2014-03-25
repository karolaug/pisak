from gi.repository import Clutter
from pisak import widgets

class RewardPanel(Clutter.Actor):
    def __init__(self, container):
        super().__init__()
        self.container = container
        layout = Clutter.BinLayout()
        self.set_layout_manager(layout)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.set_reactive(True)
        self.connect('button_release_event', lambda x,y: self.exit_panel())
        self._init_elements()

    def _init_elements(self):
        self._init_reward_info()
        self._init_reward()

    def _init_reward_info(self):
        self.reward_info = widgets.TextField()
        self.add_actor(self.reward_info)

    def _init_reward(self):
        pass #self.reward = song/movie

    def run_reward(self, reward_file_path):
        pass #self.reward.play

    def set_reward_info(self, reward_info):
        self.reward_info.set_text(reward_info)

    def set_font(self, font_name):
        self.reward_info.set_font(font_name)

    def exit_panel(self):
        self.container.change_panel()

class ResultInfoPanel(Clutter.Actor):
    def __init__(self, container):
        super().__init__()
        self.container = container
        layout = Clutter.BinLayout()
        self.set_layout_manager(layout)
        self.set_y_expand(True)
        self.set_x_expand(True)
        self.set_reactive(True)
        self.connect('button_release_event', lambda x,y: self.exit_panel())
        self._init_result_info()

    def _init_result_info(self):
        self.result_info = widgets.TextField()
        self.add_actor(self.result_info)

    def set_result_info(self, result_info):
        self.result_info.set_text(result_info)

    def set_font(self, font_name):
        self.result_info.set_font(font_name)

    def exit_panel(self):
        self.container.change_panel()

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
