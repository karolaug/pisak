from gi.repository import Clutter
from pisak.speller.widgets import Text

class Cursor():
    pass

class TestText(Text):
    def __init__(self):
        super().__init__()

        self.set_background_color(Clutter.Color.new(0, 255, 0, 255))

        self.clutter_text.set_size(400, 200)
        self.clutter_text.set_cursor_visible(True)
        self.clutter_text.set_cursor_size(5)
        self.clutter_text.set_text("isjdbf")
        self.clutter_text.set_cursor_position(2)
        self.clutter_text.set_reactive(True)
        self.clutter_text.set_editable(True)
        self.clutter_text.set_cursor_color(Clutter.Color.new(255, 255, 0, 255))

        self.clutter_text.set_cursor_size(5)

class TextStage(Clutter.Stage):
    
    def __init__(self):
        super().__init__()

        self.set_title("TextApp")
        self.set_size(800, 600)
        self.set_background_color(Clutter.Color.new(255, 0, 0, 255))

        self.text = TestText()

        self.pos = Clutter.Text()
        self.pos2 = Clutter.Text()
        self.pos.set_background_color(Clutter.Color.new(0, 0, 255, 255))

        cursor_pos = self.text.clutter_text.get_cursor_position()
        coords = self.text.clutter_text.position_to_coords(cursor_pos)        

        self.pos.set_text(''.join(["Kursor na pozycji: ", str(cursor_pos)]))
        self.pos2.set_text(''.join(["Kursor na koordynatach: ", str(coords)]))

        self.layout = Clutter.BoxLayout()
        self.layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.add_child(self.pos)
        self.add_child(self.text)
        self.add_child(self.pos2)
        self.set_layout_manager(self.layout)

        self.connect("button_press_event", lambda _1, _2: self.onKeyPress(_1, _2))

    def onKeyPress(self, event, button):
        cursor_pos = self.text.clutter_text.get_cursor_position()
        self.text.clutter_text.insert_text("k", cursor_pos)
        self.pos.set_text(''.join(["Kursor na pozycji: ", str(cursor_pos)]))
        coords = self.text.clutter_text.position_to_coords(cursor_pos)
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
