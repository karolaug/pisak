from gi.repository import Clutter

class Cursor():
    pass

class TestText(Clutter.Text):
    def __init__(self):
        super().__init__()

        self.set_background_color(Clutter.Color.new(0, 255, 0, 255))

        self.set_cursor_visible(True)
        self.set_cursor_size(5)
        self.set_text("isjdbf")
        self.set_cursor_position(2)
        self.set_reactive(True)
        self.set_editable(True)
        self.set_cursor_color(Clutter.Color.new(255, 255, 0, 255))

        self.set_cursor_size(5)

class TextStage(Clutter.Stage):
    def __init__(self):
        super().__init__()

        self.set_title("TextApp")
        self.set_size(800, 600)

        self.text = TestText()

        self.pos = Clutter.Text()
        self.pos2 = Clutter.Text()
        self.pos.set_background_color(Clutter.Color.new(0, 0, 255, 255))

        cursor_pos = self.text.get_cursor_position()
        coords = self.text.position_to_coords(cursor_pos)        

        self.pos.set_text(''.join(["Kursor na pozycji: ", str(cursor_pos)]))
        self.pos2.set_text(''.join(["Kursor na koordynatach: ", str(coords)]))

        self.layout = Clutter.BoxLayout()
        self.layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.add_child(self.pos)
        self.add_child(self.text)
        self.add_child(self.pos2)
        self.set_layout_manager(self.layout)

        self.text.connect("cursor_changed",
                          lambda _1: self.onKeyPress(_1))

    def onKeyPress(self, event):
        cursor_pos = self.text.get_cursor_position()
        self.pos.set_text(''.join(["Kursor na pozycji: ", str(cursor_pos)]))
        coords = self.text.position_to_coords(cursor_pos)
        self.pos2.set_text(''.join(["Kursor na koordynatach: ", str(coords)]))

class TextApp(object):
    def __init__(self):
        Clutter.init()

        self.stage = TextStage()
        self.stage.connect("destroy", lambda *_: Clutter.main_quit())
        self.stage.show_all()

        Clutter.main()

if __name__ == '__main__':
    TextApp()
