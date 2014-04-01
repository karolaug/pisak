from gi.repository import Clutter

class AbstractViewContainer(object):
    def __init__(self, context):
        super().__init__()
        self.context = context
        self._view_stack = []
    
    def push_view(self, view):
        self._view_stack.append(view)
        self._post_push_view(view)
    
    def pop_view(self):
        self._pre_pop_view(self._view_stack[-1])
        self._view_stack.pop()
    
    def _post_push_view(self, view):
        raise NotImplementedError()
    
    def _pre_pop_view(self, view):
        raise NotImplementedError()


class BasicViewContainer(AbstractViewContainer, Clutter.Actor):
    def __init__(self, context):
        super().__init__(context)
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)
        self._current_view = Clutter.Actor()
        self.add_child(self._current_view)
    
    def _post_push_view(self, view):
        self.remove_child(self._current_view)
        self._current_view = view
        self.add_child(self._current_view)
        
    def _pre_pop_view(self, view):
        self.remove_child(self._current_view)
        self._current_view = self._view_stack[-1] if self._view_stack else Clutter.Actor()
        self.add_child(self._current_view)

