import unittest
from gi.repository import Clutter
import view
import tests.clutter

class AbstractViewContainerTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])

    def test_abstract_view_container(self):
        """
        Abstract view container methods
        """
        context = object()
        view_container = view.AbstractViewContainer(context)
        view_actor = object()
        with self.assertRaises(NotImplementedError):
            view_container.push_view(view_actor)
        with self.assertRaises(NotImplementedError):
            view_container.pop_view()
     
    def test_dummy_view_container(self):
        """
        View container usage
        """
        pushed = False
        popped = False
        class DummyViewContainer(view.AbstractViewContainer):
            def _post_push_view(self, view):
                nonlocal pushed
                pushed = True

            def _pre_pop_view(self, view):
                nonlocal popped
                popped = True

        context = object()
        view_actor = object()
        view_container = DummyViewContainer(context)
        view_container.push_view(view_actor)
        self.assertTrue(pushed)
        view_container.pop_view()
        self.assertTrue(popped)
   
    @tests.clutter.on_stage
    def test_basic_view_container(self, stage):
       """
       View container as clutter actor
       """
       context = object()
       view_container = view.BasicViewContainer(context)
       view_actor_1 = Clutter.Actor()
       view_actor_2 = Clutter.Actor()
       stage.add_child(view_container)
       view_container.push_view(view_actor_1)
       view_container.push_view(view_actor_2)
       view_container.pop_view()


if __name__ == '__main__':
    unittest.main()
