'''
Test tile handler property in paged tile view
'''
import unittest
from gi.repository import Clutter
from pisak import widgets


class TileHandlerTest(unittest.TestCase):
    MODEL = {
        "items": [
            {"label": "a"}, {"label": "b"},
            {"label": "c"}, {"label": "d"}],
        "page_interval": 3000}

    def setUp(self):
        Clutter.init([])

    def test_tile_handler(self):
        self.activated = False
        def handler(tile):
            self.activated = True
        view_actor = widgets.PagedTileView()
        view_actor.set_model(self.MODEL)
        view_actor.tile_handler = handler
        page = view_actor.generate_page(0)
        page.tiles[0].emit("activate")
        self.assertTrue(self.activated, "Handler not set up properly")

    def test_bad_handler(self):
        view_actor = widgets.PagedTileView()
        with self.assertRaises(ValueError, msg="Handler not checked for callablity"):
            view_actor.tile_handler = object()


if __name__ == "__main__":
    unittest.main()
