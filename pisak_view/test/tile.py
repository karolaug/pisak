import unittest
import widgets
from gi.repository import Clutter, GObject

def on_stage(function):
    def ret(*args):
        stage = Clutter.Stage()
        args = args + (stage,)
        function(*args)
        stage.destroy()
    return ret

class TileTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])
        
    @on_stage
    def test_create(self, stage):
        tile = widgets.Tile()
        tile.set_label("test")
        stage.add_child(tile)
    
    @on_stage
    def test_model(self, stage):
        model = {"label": "label"}
        tile = widgets.Tile()
        stage.add_child(tile)
        tile.set_model(model)
    
    @on_stage
    def test_model_bad(self, stage):
        model = {"label": "label", "image_path": "/../nonexistent"}
        tile = widgets.Tile()
        stage.add_child(tile)
        with self.assertRaises(GObject.GError):
            tile.set_model(model)
    
    def test_hilite(self):
        tile = widgets.Tile()
        tile.hilite_off()
        tile.hilite_on()
        tile.hilite_on()
        tile.hilite_off()

class PagedTileViewTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])
    
    @on_stage
    def test_create(self, stage):
        view = widgets.PagedTileView()
        stage.add_child(view)
        stage.destroy()
    
    @on_stage
    def test_model(self, stage):
        view = widgets.PagedTileView()
        model = {"items": [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}], "page_interval": 3000}
        view.set_model(model)
        
class TilePageTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])
        
    @on_stage
    def test_create(self, stage):
        items = [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}]
        page = widgets.TilePage(items, 0)
        stage.add_child(page)
        stage.destroy()
    
    def test_instatiate_cycle(self):
        items = [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}]
        page = widgets.TilePage(items, 0)
        cycle = widgets._TilePageCycle(page)
        cycle.select()
    
    @on_stage
    def test_cycle(self, stage):
        items = [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}]
        page = widgets.TilePage(items, 0)
        cycle = page.create_cycle()
        cycle.expose_next()
        cycle.expose_next()
        cycle.stop()
    
    def test_expire(self):
        items = [{"label": "a"}, {"label": "b"}, {"label": "c"}, {"label": "d"}]
        page = widgets.TilePage(items, 0)
        cycle = page.create_cycle()
        for _ in range(len(items) * 2 - 1):
            has_more = cycle.expose_next()
            self.assertTrue(has_more)
        has_more = cycle.expose_next()
        self.assertFalse(has_more)
            

if __name__ == '__main__':
    unittest.main()
