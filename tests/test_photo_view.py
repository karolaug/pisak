'''
Test for single photo view
'''
import unittest
from gi.repository import Clutter, GObject, Mx
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
        Create and empty photo view
        """
        dummy_context = object()
        view_actor = application.PhotoView(dummy_context)
        stage.add_child(view_actor)
    
    def test_model(self):
        """
        Set model in photo view
        """
        dummy_context = object()
        view_actor = application.PhotoView(dummy_context)
        model = {
            "items": [
                {"photo_path": os.path.join(res.PATH, "krolikarnia.jpg")},
                {"photo_path": os.path.join(res.PATH, "jagoda.jpg")}],
            "initial_photo": 0,
            "start_slideshow": False
        }
        view_actor.set_model(model)
        
        has_slide = False
        for child in view_actor.get_children():
            has_slide = has_slide or isinstance(child, widgets.PhotoSlide)
        self.assertTrue(has_slide, "Photo view has no slide") 
    
    @tests.clutter.on_stage
    def test_photo_slide(self, stage):
        """
        Set model in photo slide
        """
        model_1 = {"photo_path": os.path.join(res.PATH, "krolikarnia.jpg")}
        model_2 = {"photo_path": "/../nonexistent"}
        model_3 = {"photo_path": "/dev/null"}
        actor = widgets.PhotoSlide()
        
        actor.set_model(model_1)
        has_image = False
        for child in actor.get_children():
            has_image = has_image or isinstance(child, Mx.Image)
        self.assertTrue(has_image, "Photo slide has no image")
        
        with self.assertRaises(GObject.GError, msg="Nonexistent image path accepted"):
            actor.set_model(model_2)
        
        with self.assertRaises(GObject.GError, msg="Invalid image file accepted"):
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