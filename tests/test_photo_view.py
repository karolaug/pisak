'''
Test for single photo view
'''
import unittest
from gi.repository import Clutter, GObject
import tests.clutter
from pisak.viewer import application
from pisak import widgets, res, switcher_app
import os.path

class PhotoViewTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])

    @tests.clutter.on_stage
    def test_create(self, stage):
        """
        Create photo view
        """
        dummy_context = object()
        view_actor = application.PhotoView(dummy_context)
        stage.add_child(view_actor)
    
    def test_model(self):
        """
        Photo view model
        """
        dummy_context = object()
        view_actor = application.PhotoView(dummy_context)
        model = {
            "items": ["photo 1", "photo 2", "photo 3"],
            "initial_photo": 0,
            "start_slideshow": False
        }
        view_actor.set_model(model)
    
    @tests.clutter.on_stage
    def test_photo_slide(self, stage):
        """
        Photo slide model
        """
        model_1 = {"photo_path": os.path.join(res.PATH, "krolikarnia.jpg")}
        model_2 = {"photo_path": "/../nonexistent"}
        model_3 = {"photo_path": "/dev/null"}
        actor = widgets.PhotoSlide()
        actor.set_model(model_1)
        with self.assertRaises(GObject.GError):
            actor.set_model(model_2)
        with self.assertRaises(GObject.GError):
            actor.set_model(model_3)
    
    def test_photo_cycle(self):
        dummy_context = object()
        view_actor = application.PhotoView(dummy_context)
        
        cycle_1 = view_actor.create_idle_cycle()
        self.assertIsInstance(cycle_1, switcher_app.Cycle)
        self.assertTrue(cycle_1.has_next())
        cycle_1.expose_next()
        self.assertTrue(cycle_1.has_next())
        cycle_1.select()
        
        cycle_2 = view_actor.create_slideshow_cycle()
        self.assertIsInstance(cycle_2, switcher_app.Cycle)
        self.assertFalse(cycle_2.has_next())


if __name__ == "__main__":
    unittest.main()