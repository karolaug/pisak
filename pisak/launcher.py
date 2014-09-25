'''
Module which processes and launches pisak apps
'''
import sys

from gi.repository import Clutter

from pisak import switcher_app, signals, unit

import pisak.layout  # @UnusedImport
import pisak.widgets  # @UnusedImport
import pisak.handlers  # @UnusedImport
import pisak.speller.handlers # @UnusedImport
from pisak.viewer import widgets, handlers  # @UnusedImport
import pisak.symboler.widgets  # @UnusedImport
from pisak.main_panel import widgets  # @UnusedImport

class LauncherError(Exception):
    """
    Error thrown when launcher meets an unexcpected condition.
    """
    pass


class LauncherStage(Clutter.Stage):
    def __init__(self, descriptor):
        super().__init__()
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self.views = descriptor.get("views")
        self.initial = descriptor.get("initial-view")
        self.initial_data = descriptor.get("initial-data")
        self.load_view(self.initial, self.initial_data)

    def load_view(self, name, data):
        if name not in self.views.keys():
            message = "Descriptor has no view with name: {}".format(name)
            raise LauncherError(message)
        view_path, prepare = self.views.get(name)
        self.script = Clutter.Script()
        self.script.load_from_file(view_path)
        self.script.connect_signals_full(signals.connect_registered)
        prepare(self, self.script, data)
        children = self.get_children()
        main_actor = self.script.get_object("main")
        if children:
            old_child = children[0]
            self.replace_child(old_child, main_actor)
        else:
            self.add_child(main_actor)


def run(descriptor):
    # nested class to inject app descriptor
    class LauncherApp(switcher_app.Application):
        '''
        Implementation of switcher app for JSON descriptors.
        '''
        def create_stage(self, argv):
            stage = LauncherStage(descriptor)
            stage.set_size(unit.size_pix[0], unit.size_pix[1])
            stage.set_fullscreen(True)
            return stage

    app = LauncherApp(sys.argv)
    app.main()
