'''
Module which processes and launches brain flippers
'''
from pisak import switcher_app
from gi.repository import Clutter
import sys

import pisak.layout  # @UnusedImport
import pisak.widgets  # @UnusedImport
import brain_flippers.widgets  # @UnusedImport
import brain_flippers.digit_span.widgets  # @UnusedImport
import brain_flippers.malpa.widgets # @UnusedImport
import brain_flippers.bomba.widgets # @UnusedImport

class LauncherStage(Clutter.Stage):
    def __init__(self, context, descriptor):
        super().__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.views = descriptor.get("views")
        self.initial = descriptor.get("initial-view")
        color = descriptor.get("background-color")
        if color:
            self.set_background_color(Clutter.Color.from_string(color)[1])
        initial_data = descriptor.get("initial-data")
        self.load_view(self.initial, initial_data)

    def load_view(self, name, data):
        view_path, prepare = self.views.get(name)
        self.script = Clutter.Script()
        self.script.load_from_file(view_path)
        prepare(self, self.script, data)
        main_actor = self.script.get_object("main")
        self.remove_all_children()
        self.add_child(main_actor)


def run(descriptor):
    # nested class to inject app descriptor
    class LauncherApp(switcher_app.Application):
        '''
        Implementation of switcher app for JSON descriptors.
        ''' 
        def create_stage(self, argv):
            stage = LauncherStage(self.context, descriptor)
            stage.set_size(1366, 768)
            stage.set_fullscreen(True)
            return stage
    
    app = LauncherApp(sys.argv)
    app.main()
