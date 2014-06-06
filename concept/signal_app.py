import sys
from pisak import switcher_app
from gi.repository import Clutter, Mx, GObject
from pisak import signals


class ButtonStage(Clutter.Stage):
    '''
    Clutter stage with single button in the center
    '''
    def __init__(self):
        super().__init__()
        Mx.Style.get_default()
        script = Clutter.Script()
        script.load_from_file("signals.json")
        script.connect_signals_full(signals.python_connect)
        main_actor = script.get_object("main")
        self.add_child(main_actor)
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        return ButtonStage()
        

if __name__ == '__main__':
    ButtonApp(sys.argv).main()