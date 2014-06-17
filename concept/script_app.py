#!/usr/bin/env python3
'''
JSON script tester app
'''
import sys
from pisak import switcher_app
from gi.repository import Clutter

import pisak.scanning  # @UnusedImport
import pisak.layout  # @UnusedImport
import brain_flippers.safe.widgets  # @UnusedImport


class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def usage(self, argv):
        print("Usage:")
        print(argv[0] + " JSON_PATH")

    def create_stage(self, argv):
        if len(argv) != 2:
            self.usage(argv)
            sys.exit(1)
        script_path = argv[1]
        script = Clutter.Script()
        try:
            script.load_from_file(script_path)
        except:
            print("Failed to load script.")
            exit(2)
        stage = Clutter.Stage()
        stage.set_layout_manager(Clutter.BinLayout())
        stage.add_child(script.get_object("main"))
        return stage


if __name__ == '__main__':
    ButtonApp(sys.argv).main()
