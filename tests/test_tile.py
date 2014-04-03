import unittest
from pisak import widgets, switcher_app
import tests.clutter
from gi.repository import Clutter, GObject

class TileTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])
        
    @tests.clutter.on_stage
    def test_create(self, stage):
        """
        Create a tile
        """
        tile = widgets.Tile()
        tile.set_label("test")
        stage.add_child(tile)
    
    @tests.clutter.on_stage
    def test_model(self, stage):
        """
        Initialize a tile with a model.
        """
        model = {"label": "label"}
        tile = widgets.Tile()
        stage.add_child(tile)
        tile.set_model(model)
    
    @tests.clutter.on_stage
    def test_model_bad(self, stage):
        """
        Initialize a tile with an invalid model.
        """
        model = {"label": "label", "image_path": "/../nonexistent"}
        tile = widgets.Tile()
        stage.add_child(tile)
        with self.assertRaises(GObject.GError):
            tile.set_model(model)
    
    def test_hilite(self):
        """
        Highlight a tile.
        """
        tile = widgets.Tile()
        tile.hilite_off()
        tile.hilite_on()
        tile.hilite_on()
        tile.hilite_off()


class PagedTileViewTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])
    
    @tests.clutter.on_stage
    def test_create(self, stage):
        """
        Create a paged tile view.
        """
        view = widgets.PagedTileView()
        stage.add_child(view)
        stage.destroy()
    
    @tests.clutter.on_stage
    def test_model(self, stage):
        """
        Initialize a paged tile view with a model.
        """
        view = widgets.PagedTileView()
        model = {"items": [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}], "page_interval": 3000}
        view.set_model(model)
    
    def test_cycle(self):
        view = widgets.PagedTileView()
        model = {"items": [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}], "page_interval": 3000}
        view.set_model(model)
        cycle = view.create_cycle()
        for _ in range(3 * len(model["items"])):
            self.assertTrue(cycle.has_next())
            cycle.expose_next()
        # the cycle is infinite
        self.assertTrue(cycle.has_next())
        cycle.stop()


class TilePageTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])
        
    @tests.clutter.on_stage
    def test_create(self, stage):
        """
        Create a tile page.
        """
        items = [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}]
        page = widgets.TilePage(items, 0)
        stage.add_child(page)
        stage.destroy()
    
    def test_instatiate_cycle(self):
        """
        Get a cycle from a tile page.
        """
        items = [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}]
        page = widgets.TilePage(items, 0)
        cycle = widgets._TilePageCycle(page)
        cycle.has_next()
        
    def test_select_cycle(self):
        """
        Test cycle selection
        """
        pushed = False
        class DummyApplication(object):
            def push_view(self, view):
                nonlocal pushed
                pushed = True
        
        items = [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}]
        page = widgets.TilePage(items, 0)
        cycle = widgets._TilePageCycle(page)
        cycle.expose_next()
        selection = cycle.select()
        dummy_application = DummyApplication()
        dummy_context = switcher_app.Context(dummy_application)
        selection(dummy_context)
        self.assertTrue(pushed)
    
    @tests.clutter.on_stage
    def test_cycle(self, stage):
        """
        Cycle exposing and stopping.
        """
        items = [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}]
        page = widgets.TilePage(items, 0)
        cycle = page.create_cycle()
        cycle.expose_next()
        cycle.expose_next()
        cycle.stop()
    
    def test_expire(self):
        """
        Cycle expiration after 2 rounds.
        """
        items = [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}]
        page = widgets.TilePage(items, 0)
        cycle = page.create_cycle()
        for _ in range(len(items) * 2):
            self.assertTrue(cycle.has_next())
            cycle.expose_next()
        self.assertFalse(cycle.has_next())
            

if __name__ == '__main__':
    unittest.main()

