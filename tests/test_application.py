import unittest
from gi.repository import Clutter
from pisak import switcher_app
from pisak.viewer import application

class ViewerContainerTests(unittest.TestCase):
    def setUp(self):
        Clutter.init([])

    def test_context(self):
        class DummyApplication(object):
            def __init__(self):
                self.context = switcher_app.Context(self)
        
        dummy_app = DummyApplication()
        context = dummy_app.context
        self.assertEqual(dummy_app, context.application)
        self.assertIsInstance(context.switcher, switcher_app.Switcher)
        
    def test_content(self):
        context = switcher_app.Context(object())
        content = application.PisakViewerContainer(context)
        cycle = content.create_cycle()
        cycle.expose_next()
        cycle.expose_next()
        cycle.stop()
    
    def test_views(self):
        view_1 = Clutter.Actor()
        view_2 = Clutter.Actor()
        context = switcher_app.Context(object())
        content = application.PisakViewerContainer(context)
        content.push_view(view_1)
        content.push_view(view_2)

class ApplicationTests(unittest.TestCase):
    def setUp(self):
        Clutter.init([])
    
    def test_push_view(self):
        dummy_view = Clutter.Actor()
        viewer_app = application.PisakViewApp([])
        viewer_app.push_view(dummy_view)

if __name__ == '__main__':
    unittest.main()
