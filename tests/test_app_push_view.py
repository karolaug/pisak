'''
Test inserting and removing view in application
'''
import unittest
from pisak.viewer import application
from gi.repository import Clutter
from pisak import switcher_app

class TestAppView(unittest.TestCase):
    def setUp(self):
        Clutter.init([])

    def test_push_view(self):
        class DummyCycle(switcher_app.Cycle):
            interval = 1000
            
            def expose_next(self):
                pass
            
            def stop(self):
                pass

        class ViewActor(Clutter.Actor):
            def create_initial_cycle(self):
                return DummyCycle()
            
        app = application.PisakViewApp([])
        view_1 = ViewActor()
        view_2 = ViewActor()
        app.push_view(view_1)
        app.push_view(view_2)
        self.assertGreater(len(app.context.switcher.cycle_stack), 2, "App does not handle view cycles")
    

if __name__ == "__main__":
    unittest.main()