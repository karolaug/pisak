import unittest
from pisak.widgets import PagedTileView
from pisak import switcher_app

class CycleSelectionTest(unittest.TestCase):
    def test_page_tile_view(self):
        dummy_application = object()
        dummy_context = switcher_app.Context(dummy_application)
        model = {"items": [{"label": "a"}], "page_interval": 3000}
        actor = PagedTileView()
        actor.set_model(model)
        cycle = actor.create_cycle()

        selection = cycle.select()
        selection(dummy_context)
