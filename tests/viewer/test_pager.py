'''
Pager widget tests
'''
import unittest
from gi.repository import Clutter, GObject
from pisak import pager, scanning


class Test(unittest.TestCase):
    def setUp(self):
        Clutter.init([])

    def test_groups(self):
        """Test pager widget group generation"""
        parent_group = scanning.Group()
        pager_actor = pager.PagerWidget()
        parent_group.add_child(pager_actor)
        subgroups = list(parent_group.get_subgroups())
        self.assertEqual(subgroups, [], "Failed to get valid subgroups")
    
    def test_data_source(self):
        pager_actor = pager.PagerWidget()
        data_source = pager_actor.get_property("data-source")
        self.assertEqual(data_source, None, "Incorrect initialization")
        data_source = pager.DataSource()
        pager_actor.set_property("data-source", data_source)
        stored_source = pager_actor.get_property("data-source")
        self.assertEqual(data_source, stored_source, "Incorrect setter")


if __name__ == "__main__":
    unittest.main()
