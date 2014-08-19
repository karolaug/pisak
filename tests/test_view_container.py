import unittest
from gi.repository import Clutter
from pisak import view, switcher_app
import tests.clutter

class DummyViewContainer(view.AbstractViewContainer):
    def __init__(self, context):
        super().__init__(context)
        self.pushed = self.popped = False

    def _post_push_view(self, view):
        self.pushed = True

    def _pre_pop_view(self, view):
        self.popped = True


class DummyView(object):
    def create_initial_cycle(self):
        return DummyCycle()


class DummyCycle(switcher_app.Cycle):
    interval = 100
    def expose_next(self):
        pass

    def stop(self):
        pass

    def has_next(self):
        return True


class AbstractViewContainerTest(unittest.TestCase):
    def setUp(self):
        Clutter.init([])

    def test_abstract_view_container(self):
        """
        Abstract view container methods
        """
        context = switcher_app.Context(object())
        view_container = view.AbstractViewContainer(context)
        view_actor = DummyView()
        with self.assertRaises(NotImplementedError):
            view_container.push_view(view_actor)
        with self.assertRaises(NotImplementedError):
            view_container.pop_view()

    def test_dummy_view_container(self):
        """
        View container usage
        """
        context = switcher_app.Context(object())
        view_actor = DummyView()
        view_container = DummyViewContainer(context)
        view_container.push_view(view_actor)
        self.assertTrue(view_container.pushed)
        view_container.pop_view()
        self.assertTrue(view_container.popped)

    @tests.clutter.on_stage
    def test_basic_view_container(self, stage):
        """
        View container as clutter actor
        """
        class DummyViewActor(Clutter.Actor):
            def create_initial_cycle(self):
                return DummyCycle()

        context = switcher_app.Context(object())
        view_container = view.BasicViewContainer(context)
        view_actor_1 = DummyViewActor()
        view_actor_2 = DummyViewActor()
        stage.add_child(view_container)
        view_container.push_view(view_actor_1)
        view_container.push_view(view_actor_2)
        view_container.pop_view()


if __name__ == '__main__':
    unittest.main()
