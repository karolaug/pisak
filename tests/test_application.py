import unittest
import time
from gi.repository import GObject, Clutter
from pisak import switcher_app
from pisak.viewer import application

class ViewerContainerTests(unittest.TestCase):
    def test_context(self):
        class DummyApplication(object):
            def __init__(self):
                self.context = switcher_app.Context(self)
        
        dummy_app = DummyApplication()
        context = dummy_app.context
        self.assertEqual(dummy_app, context.application)
        self.assertIsInstance(context.switcher, switcher_app.Switcher)
        
    def test_content(self):
        Clutter.init([])
        content = application.PisakViewerContainer()
        cycle = content.create_cycle()
        cycle.expose_next()
        cycle.expose_next()
        cycle.stop()


if __name__ == '__main__':
    unittest.main()
