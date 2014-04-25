from gi.repository import Clutter
from pisak import unit, buttons, view, switcher_app


class TextView(Clutter.Text):
    """
    Widget for displaying text.
    """
    def __init__(self):
        super().__init__()
        self.set_x_expand(True)
        self.set_y_expand(True)
        color = Clutter.Color.new(245, 245, 245, 255)
        self.set_background_color(color)
        self.set_font_name('monospace normal 20')
        self.set_text("Nierówny dostęp...")


class KeyboardMenu(Clutter.Actor):
    """
    Widget of functional buttons closely related to Keyboard.
    """
    BUTTONS = [{
        "label": "%s" % i,
        "icon_path": "%s" % j,
        "handler": k
        } for i,j,k in [
            ["02", None, None], ["_", None, None], ["ABCX", None, None],
            ["a->A", None, None], ["A->Ą", None, None], [":-)", None, None], ["01", None, None]
            ]
    ]
    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_buttons()
        
    def _init_layout(self):
        self.set_x_expand(True)
        self.set_y_expand(True)
        self.layout = Clutter.GridLayout()
        self.layout.set_column_spacing(unit.mm(2))
        self.layout.set_column_homogeneous(True)
        self.set_layout_manager(self.layout)

    def _init_buttons(self):
        for i in range(7):
            button = buttons.FramedButtonType1()
            button.set_x_expand(True)
            button.set_y_expand(True)
            button.set_model(self.BUTTONS[i])
            if i < 2:
                self.layout.attach(button, i, 0, 1, 1)
            elif i == 2:
                self.layout.attach(button, i, 0, 2, 1)
            elif i == 3:
                self.layout.attach(button, i+1, 0, 2, 1)
            elif i == 4:
                self.layout.attach(button, i+2, 0, 2, 1)
            elif i > 4:
                self.layout.attach(button, i+3, 0, 1, 1)
                
    
class Keyboard(Clutter.Actor):
    """
    Widget of buttons necessary for entering text.
    """
    BUTTONS = [{
        "label": "%s" % i
        } for i in [
            "Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
            "A", "S", "D", "F", "G", "H", "J", "K", "L", "CH",
            "Z", "X", "C", "V", "B", "N", "M", "CZ", "SZ", "RZ"
            ]
    ]
    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_elements()

    def _init_layout(self):
        self.set_x_expand(True)
        self.set_y_expand(True)
        self.layout = Clutter.GridLayout()
        self.layout.set_column_spacing(unit.mm(2))
        self.layout.set_row_spacing(unit.mm(2))
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.set_layout_manager(self.layout)

    def _init_elements(self):
        self._init_menu()
        self._init_buttons()

    def _init_menu(self):
        menu = KeyboardMenu()
        self.layout.attach(menu, 0, 0, 10, 1)

    def _init_buttons(self):
        for i in range(30):
            button = buttons.FramedButtonType1()
            button.set_x_expand(True)
            button.set_y_expand(True)
            button.set_model(self.BUTTONS[i])
            x0, y0 = i%10, i/10 + 1
            self.layout.attach(button, x0, y0, 1, 1)
        
        
class Extra(Clutter.Actor):
    """
    Widget of buttons containing suggested words or other extra features.
    """
    BUTTONS = [{
        "label": "PREDYKCJA %d" % i
        } for i in reversed(range(1, 10))
    ]
    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_buttons()

    def _init_layout(self):
        self.set_x_expand(True)
        self.set_y_expand(True)
        layout = Clutter.BoxLayout()
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        layout.set_spacing(unit.mm(2))
        self.set_layout_manager(layout)

    def _init_buttons(self):
        for i in range(9):
            button = buttons.FramedButtonType1()
            button.set_x_expand(True)
            button.set_y_expand(True)
            button.set_model(self.BUTTONS[i])
            self.add_child(button)


class Menu(Clutter.Actor):
    """
    Widget of functional menu buttons.
    """
    BUTTONS = [{
        "label": "%s" % i,
        "icon_path": "%s" % j,
        "handler": k
        } for i,j,k in [
            ["KLAWIATURA", None, None], ["PREDYKCJA", None, None], ["PRZECZYTAJ", None, None],
            ["ZAPISZ", None, None], ["WCZYTAJ", None, None], ["WYŚLIJ", None, None],
            ["DRUKUJ", None, None], ["NOWY DOKUMENT", None, None], ["PANEL STARTOWY", None, None]
            ]
    ]
    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_buttons()

    def _init_layout(self):
        self.set_x_expand(True)
        self.set_y_expand(True)
        layout = Clutter.BoxLayout()
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        layout.set_spacing(unit.mm(2))
        self.set_layout_manager(layout)

    def _init_buttons(self):
        for i in range(9):
            button = buttons.FramedButtonType1()
            button.set_x_expand(True)
            button.set_y_expand(True)
            button.set_model(self.BUTTONS[i])
            self.add_child(button)


class MainView(Clutter.Actor):
    """
    Speller main view containing all the elements.
    @param context switcher application context passed from application
    """
    def __init__(self, context):
        super().__init__()
        self._init_layout()
        self._init_elements()

    def _init_layout(self):
        self.set_x_expand(True)
        self.set_y_expand(True)
        margin = Clutter.Margin()
        margin.top = margin.bottom = margin.left = margin.right = unit.mm(5)
        self.set_margin(margin)
        self.layout = Clutter.GridLayout()
        self.layout.set_column_spacing(unit.mm(4))
        self.layout.set_row_spacing(unit.mm(4))
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.set_layout_manager(self.layout)

    def _init_elements(self):
        self.menu = Menu()
        self.extra = Extra()
        self.keyboard = Keyboard()
        self.text_view = TextView()
        self._arrange_elements()

    def _arrange_elements(self):
        self.layout.attach(self.menu, 0, 0, 3, 9)
        self.layout.attach(self.extra, 3, 0, 2, 9)
        self.layout.attach(self.text_view, 5, 0, 10, 5)
        self.layout.attach(self.keyboard, 5, 5, 10, 4)

    def create_initial_cycle(self):
        return MainViewCycle(self)


class MainViewCycle(switcher_app.Cycle):
    interval = 1000
    def __init__(self, actor):
        super().__init__()
        self.actor = actor
        self.index = 0
    
    def expose_next(self):
        pass
    
    def stop(self):
        pass
    
    def has_next(self):
        return True
    
    def show_menu(self):
        pass
    
    def show_page(self):
        pass
    
    def next_page(self):
        pass


class PisakSpellerContainer(view.BasicViewContainer):
    def __init__(self, context):
        """
        Application container, which creates other widgets.
        @param contect switcher application context passed from application
        """
        super().__init__(context)


class PisakSpellerStage(Clutter.Stage):
    def __init__(self, context):
        """
        Clutter stage which sets up the switcher application.
        @param context switcher application context passed from application
        """
        super(PisakSpellerStage, self).__init__()
        self.context = context
        self._init_layout()
        self._init_content()
        self._init_input()

    def _init_layout(self):
        self.layout = Clutter.BinLayout()
        self.set_layout_manager(self.layout)

    def _init_content(self):
        self.content = PisakSpellerContainer(self.context)
        self.add_child(self.content)
        main = MainView(self.context)
        self.content.push_view(main)

    def _init_input(self):
        self.input = switcher_app.KeyboardSwitcherInput(self)
        self.context.switcher.add_input(self.input)
        

class PisakSpellerApp(switcher_app.Application):
    """
    Pisak speller app with pisak speller stage.
    """
    def create_stage(self, argv):
        stage = PisakSpellerStage(self.context)
        stage.set_fullscreen(True)
        return stage
