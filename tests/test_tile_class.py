'''
Test possibility to change tile class in paged tile view
'''
import unittest
from gi.repository import Clutter
from pisak import widgets

class TileClassTest(unittest.TestCase):
    MODEL = {
        "items": [
            {"label": "a"}, {"label": "b"},
            {"label": "c"}, {"label": "d"}],
        "page_interval": 3000}
    def setUp(self):
        Clutter.init([])

    def test_good_tile(self):
        class GoodTile(widgets.Tile):
            pass
        view_actor = widgets.PagedTileView()
        view_actor.tile_class = GoodTile
        view_actor.set_model(self.MODEL)
    
    def test_bad_tile(self):
        view_actor = widgets.PagedTileView()
        with self.assertRaises(ValueError, msg="Tile subclass not checked"):
            view_actor.tile_class = object
    
    def test_tile_generated(self):
        class GoodTile(widgets.Tile):
            pass
        view_actor = widgets.PagedTileView()
        view_actor.tile_class = GoodTile
        view_actor.set_model(self.MODEL)
        tile_page = view_actor.generate_page(0)
        good_tiles = False
        for child in tile_page.get_children():
            good_tiles = good_tiles or isinstance(child, GoodTile)
        self.assertTrue(good_tiles, "Generated tiles of wrong class")


if __name__ == "__main__":
    unittest.main()