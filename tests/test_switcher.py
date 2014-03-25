import unittest
import switcher_app
import time
from gi.repository import GObject, Clutter

class SwitcherAppTest(unittest.TestCase):
    def test_context(self):
        """
        Context for a dummy application.
        """
        class DummyApp(object):
            pass
        app = DummyApp()
        context = switcher_app.Context(app)
    
    def test_switcher(self):
        """
        Create switcher and add a dummy cycle to it.
        """
        class DummyCycle(object):
            def __init__(self):
                self.exposed = False
                self.interval = 1000
            def expose_next(self):
                self.exposed = True
                
        switcher = switcher_app.Switcher()
        cycle = DummyCycle()
        switcher.push_cycle(cycle)
        self.assertTrue(cycle.exposed)
     
    def test_key_switcher_input(self):
        """
        Test keyboard input with switcher.
        """
        class DummyStage(GObject.GObject):
            __gsignals__ = {
                "key-release-event": (GObject.SIGNAL_RUN_FIRST, None, (object,))
            }
            
            def __init__(self):
                super().__init__()
            
            def trigger_key(self):
                event = Clutter.KeyEvent()
                event.keyval = 0x20
                self.emit("key-release-event", event)
                
        triggered = False
        def response(source):
            nonlocal triggered
            triggered = True
        
        stage = DummyStage()
        switcher_input = switcher_app.KeyboardSwitcherInput(stage)
        switcher_input.connect("switcher-select", response)
        stage.trigger_key()
        self.assertTrue(triggered)
     
    def test_switcher_add_input(self):
        """
        Test adding an input to a switcher.
        """
        class DummyInput(switcher_app.SwitcherInput):
            def trigger(self):
                self.emit("switcher-select")
        
        switcher = switcher_app.Switcher()
        input_1 = DummyInput()
        input_2 = DummyInput()
        switcher.add_input(input_1)
        switcher.add_input(input_2)
        switcher.remove_input(input_1)
        switcher.remove_input(input_2)
        


if __name__ == '__main__':
    unittest.main()
