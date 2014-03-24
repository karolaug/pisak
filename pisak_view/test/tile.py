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


if __name__ == '__main__':
    unittest.main()
