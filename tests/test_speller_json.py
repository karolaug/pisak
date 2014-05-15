'''
Test JSON widgets fro speller
'''
import unittest
from gi.repository import Clutter
import pisak.speller.widgets

JSON_TEMPLATE = """[
  {{
    "id": "test",
    "type": "{0}"
  }}
]
"""


TYPE_NAMES = [
    "PisakSpellerButton", "PisakSpellerKey", "PisakSpellerText",
    "PisakSpellerPrediction"]


class SpellerJSONTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])
    
    def load_json(self, text):
        script = Clutter.Script()
        script.load_from_data(text, len(text))
        self.assertGreater(len(script.list_objects()), 0)
    
    def test_loading(self):
        for type_name in TYPE_NAMES:
            json_text = JSON_TEMPLATE.format(type_name)
            self.load_json(json_text)


if __name__ == "__main__":
    unittest.main()