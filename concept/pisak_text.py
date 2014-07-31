from gi.repository import Clutter

class TextStage(Clutter.Stage):
    
    def __init__(self):
        super().__init__()

        self.set_title("TextApp")
        self.set_size(800, 600)

        self.text = Clutter.Text()
        self.text.set_cursor_visible(True)
        self.text.set_cursor_size(5)
        self.text.set_text("isjdbf")
        self.text.set_cursor_position(2)
        self.text.set_reactive(True)
        self.text.set_editable(True)

        self.layout = Clutter.BinLayout()
        self.add_child(self.text)
        self.set_layout_manager(self.layout)

        self.connect("button_press_event", lambda _1, _2: self.onKeyPress(_1, _2))

    def onKeyPress(self, event, button):
        self.text.insert_text("k", self.text.get_cursor_position())

class TextApp(object):
    def __init__(self):
        Clutter.init()

        self.stage = TextStage()
        self.stage.connect("destroy", lambda *_: Clutter.main_quit())
        self.stage.show_all()

        Clutter.main()

if __name__ == '__main__':
    TextApp()
