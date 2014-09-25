"""
Basic classes for application using switcher
"""
from gi.repository import GObject, Clutter, Mx
from pisak import res


class Application(object):
    """
    Abstract application class. This is the entry point for switcher apps.
    """

    """
    Path to default CSS style
    """
    CSS_RES_PATH = "css/default.css"

    def __init__(self, argv):
        """
        Initialize the aplication.
        :param: argv application arguments
        """
        self._initialize_stage(argv)

    def _initialize_style(self):
        # load default style
        self.style = Mx.Style.get_default()
        style_path = res.get(self.CSS_RES_PATH)
        try:
            self.style.load_from_file(style_path)
        except GObject.GError:
            raise Exception("Failed to load default style")

    def _initialize_stage(self, argv):
        # create and set up a Clutter.Stage
        Clutter.init(argv)
        self._initialize_style()
        self.stage = self.create_stage(argv)
        self.stage.connect("destroy", lambda _: Clutter.main_quit())

    def create_stage(self, argv):
        """
        Abstract method which should create Clutter.Stage instance
        :param: argv application arguments
        """
        raise NotImplementedError()

    def main(self):
        """
        Starts the application main loop.
        """
        self.stage.show_all()
        Clutter.main()
