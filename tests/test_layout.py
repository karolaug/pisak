'''
Test layout managing actors
'''
import unittest

from gi.repository import Clutter

import pisak.layout  # @UnusedImport


class TestBoxLayout(unittest.TestCase):
    BOX_JSON = """
    [
      {
        "id": "main",
        "type": "PisakBoxLayout",
        "orientation": "vertical",
        "spacing": 11
      }
    ]
    """

    def setUp(self):
        Clutter.init([])

    def test_box(self):
        """Test box layout from JSON"""
        script = Clutter.Script()
        script.load_from_data(self.BOX_JSON, len(self.BOX_JSON))
        main = script.get_object("main")
        self.assertTrue(main is not None, "Failed to load object")
        self.assertEqual(main.get_property("orientation"), Clutter.Orientation.VERTICAL)


if __name__ == "__main__":
    unittest.main()
