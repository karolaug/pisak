from gi.repository import Clutter
from cairo_cursor import Cursor
import cairo

class Cursor_Canvas(Clutter.Actor):
    def __init__(self):
        super().__init__()

        self.set_size(10, 10)
        self.canvas = Clutter.Canvas()
        self.canvas.set_size(10, 10)
        self.canvas.connect('draw', self.draw)
        self.canvas.invalidate()
        self.set_content(self.canvas)

    @staticmethod
    def draw(canvas, context, width, height):
        context.set_source_rgb(1, 0, 0)
        context.rectangle(0, 0, 10, 10)
        context.fill()
        return True

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
        self.cursor = Cursor_Canvas()
        layout = Clutter.BinLayout()
        self.container = Clutter.Actor()
        self.container.set_layout_manager(layout)
        self.container.add_child(self.text)
        self.container.add_child(self.cursor)

        self.pos = Clutter.Text()
        self.pos2 = Clutter.Text()
        self.pos.set_background_color(Clutter.Color.new(0, 0, 255, 255))

        cursor_pos = self.text.get_cursor_position()
        coords = self.text.position_to_coords(cursor_pos)

        self.pos.set_text(''.join(["Kursor na pozycji: ", str(cursor_pos)]))
        self.pos2.set_text(''.join(["Kursor na koordynatach: ", str(coords)]))

        self.layout = Clutter.BoxLayout()
        self.layout.set_orientation(Clutter.Orientation.VERTICAL)
        self.set_layout_manager(self.layout)
        self.add_child(self.pos)
        self.add_child(self.container)
        self.add_child(self.pos2)

        self.text.connect("cursor_changed",
                          lambda _1: self.onKeyPress(_1))

    def onKeyPress(self, event):
        cursor_pos = self.text.get_cursor_position()
        self.pos.set_text(''.join(["Kursor na pozycji: ", str(cursor_pos)]))
        coords = self.text.position_to_coords(cursor_pos)
        self.pos2.set_text(''.join(["Kursor na koordynatach: ", str(coords)]))
        self.cursor.set_x(coords[1])
        self.cursor.set_y(coords[2])


class TextApp(object):
    def __init__(self):
        Clutter.init()

        self.stage = TextStage()
        self.stage.connect("destroy", lambda *_: Clutter.main_quit())
        self.stage.show_all()

        Clutter.main()

if __name__ == '__main__':
    TextApp()
