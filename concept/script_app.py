'''
Does button work?
'''
import sys
from pisak import switcher_app, res
from gi.repository import Clutter
from gi.repository import Mx
from gi.repository import GObject

class DummyButton(Mx.Button):
    pass

GObject.type_register(DummyButton)

class ButtonApp(switcher_app.Application):
    '''
    Simple app written for test purposes
    '''
    def create_stage(self, argv):
        style = Mx.Style.get_default()
        style.load_from_file(res.get("style.css"))
        script = Clutter.Script()
        script.load_from_file(res.get("script.json"))
        print(script.list_objects())
        return script.get_object("stage")


if __name__ == '__main__':
    ButtonApp(sys.argv).main()