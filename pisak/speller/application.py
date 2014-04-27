from gi.repository import Clutter, Pango
from pisak import unit, buttons, view, switcher_app
from pisak.res import colors


class TextView(Clutter.Actor):
    """
    Widget for displaying text.
    """
    TXT_F_WIDTH = unit.mm(218)
    TXT_F_HEIGHT = unit.mm(108)
    MODEL = """
        Nierówny dostęp do najnowszych zdobyczy medycyny
        zaczyna dominować motywy współczesnych dystopii. W
        dziecinnie komiksowym wydaniu widać to w filmie "Elysium",
        który proponuje klasyczne dla gatunku rozwiązanie: wystarczy
        dokopać Niedobrym i Bogatym, żeby dobrodziejstwa rozlały się
        na całą ludzkość. Ale jest też prawdziwa i realna droga,
        trudniejsza i mniej widowiskowa. Prowadzi przez świat
        oprogramowania wolnego jak w słowie "wolność".
        """
    
    def __init__(self):
        super().__init__()
        color = Clutter.Color.new(250, 250, 250, 255)
        self.set_background_color(color)
        self._init_layout()
        self._init_text_field()
        self.set_model()

    def _init_layout(self):
        self.set_x_expand(True)
        self.set_x_align(Clutter.ActorAlign.CENTER)
        self.set_y_expand(True)
        self.set_y_align(Clutter.ActorAlign.END)
    
    def _init_text_field(self):
        self.text_field = Clutter.Text()
        self.text_field.set_size(self.TXT_F_WIDTH, self.TXT_F_HEIGHT)
        self.text_field.set_background_color(colors.TRANSPARENT)
        self.add_child(self.text_field)

    def set_model(self):
        self.text_field.set_line_wrap(True)
        self.text_field.set_line_alignment(Pango.Alignment.LEFT)
        self.text_field.set_font_name('normal italic 20')
        self.text_field.set_text(self.MODEL)


class ButtonBlock(Clutter.Actor):
    """
    Base class for widgets containing blocks of buttons.
    """
    
    def __init__(self):
        super().__init__()
        self._init_layout()
        self._init_buttons()

    def _init_layout(self):
        raise NotImplementedError()

    def _init_buttons(self):
        raise NotImplementedError()
    
    def hilite_on(self):
        buttons = self.get_children()
        for b in buttons:
            b.hilite_on()

    def hilite_off(self):
        buttons = self.get_children()
        for b in buttons:
            b.hilite_off()

    def select_on(self):
        buttons = self.get_children()
        for b in buttons:
            b.select_on()

            
class KeyboardMenu(ButtonBlock):
    """
    Widget of functional buttons closely related to Keyboard.
    """
    BT_WIDTH = {
        1: unit.mm(20),
        2: unit.mm(42)
        }
    BT_HEIGHT = unit.mm(20)
    SPACING = unit.mm(2)
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
        
    def _init_layout(self):
        layout = Clutter.BoxLayout()
        layout.set_orientation(Clutter.Orientation.HORIZONTAL)
        layout.set_spacing(self.SPACING)
        self.set_layout_manager(layout)

    def _init_buttons(self):
        for i in range(7):
            button = buttons.FramedButtonType1()
            if i in (2, 3, 4):
                span = 2
            else:
                span = 1
            button.set_size(self.BT_WIDTH[span], self.BT_HEIGHT)
            self.add_child(button)
            button.set_model(self.BUTTONS[i])

    
class Keyboard(Clutter.Actor):
    """
    Widget of buttons necessary for entering text.
    """
    BT_WIDTH = unit.mm(20)
    BT_HEIGHT = unit.mm(20)
    SPACING = unit.mm(2)
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
        self.set_x_align(Clutter.ActorAlign.CENTER)
        self.set_y_expand(True)
        self.set_y_align(Clutter.ActorAlign.END)
        layout = Clutter.BoxLayout()
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        layout.set_spacing(self.SPACING)
        self.set_layout_manager(layout)

    def _init_elements(self):
        self._init_menu()
        self._init_buttons()

    def _init_menu(self):
        menu = KeyboardMenu()
        self.add_child(menu)

    def _init_buttons(self):
        for i in range(30):
            if i in (0, 10, 20):
                row = Keyboard.SingleRow()
            button = buttons.FramedButtonType1()
            button.set_size(self.BT_WIDTH, self.BT_HEIGHT)
            row.add_child(button)
            button.set_model(self.BUTTONS[i])
            if i in (9, 19, 29):
                self.add_child(row)

    class SingleRow(ButtonBlock):
        SPACING =  unit.mm(2)
            
        def __init__(self):
            super().__init__()

        def _init_layout(self):
            layout = Clutter.BoxLayout()
            layout.set_orientation(Clutter.Orientation.HORIZONTAL)
            layout.set_spacing(self.SPACING)
            self.set_layout_manager(layout)

        def _init_buttons(self):
            pass

    def hilite_on(self):
        rows = self.get_children()
        for r in rows:
            r.hilite_on()

    def hilite_off(self):
        rows = self.get_children()
        for r in rows:
            r.hilite_off()

    def select_on(self):
        rows = self.get_children()
        for r in rows:
            r.select_on()


class KeyboardCycle(switcher_app.Cycle):
    interval = 1000
    
    def __init__(self, actor):
        super().__init__()
        self.actor = actor
        self.STEPS = actor.get_children()
        self.index = 0
    
    def expose_next(self):
        self.STEPS[self.index-1].hilite_off()
        self.STEPS[self.index].hilite_on()
        self.index = (self.index + 1) % len(self.STEPS)

    def select(self):
        self.STEPS[self.index-1].select_on()
        return None
    
    def has_next(self):
        return True

        
class Extra(ButtonBlock):
    """
    Widget of buttons containing suggested words or other extra features.
    """
    BT_WIDTH = unit.mm(42)
    BT_HEIGHT = unit.mm(20)
    SPACING = unit.mm(2)
    BUTTONS = [{
        "label": "PREDYKCJA %d" % i
        } for i in reversed(range(1, 10))
    ]
    
    def __init__(self):
        super().__init__()

    def _init_layout(self):
        self.set_x_expand(True)
        self.set_x_align(Clutter.ActorAlign.CENTER)
        self.set_y_expand(True)
        self.set_y_align(Clutter.ActorAlign.END)
        layout = Clutter.BoxLayout()
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        layout.set_spacing(self.SPACING)
        self.set_layout_manager(layout)

    def _init_buttons(self):
        for i in range(9):
            button = buttons.FramedButtonType1()
            button.set_size(self.BT_WIDTH, self.BT_HEIGHT)
            self.add_child(button)
            button.set_model(self.BUTTONS[i])


class ExtraCycle(switcher_app.Cycle):
    interval = 1000
    
    def __init__(self, actor):
        super().__init__()
        self.actor = actor
        self.STEPS = actor.get_children()
        self.index = 0
    
    def expose_next(self):
        self.STEPS[self.index-1].hilite_off()
        self.STEPS[self.index].hilite_on()
        self.index = (self.index + 1) % len(self.STEPS)
    
    def has_next(self):
        return True
    

class Menu(ButtonBlock):
    """
    Widget of functional menu buttons.
    """
    BT_WIDTH = unit.mm(64)
    BT_HEIGHT = unit.mm(20)
    SPACING = unit.mm(2)
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

    def _init_layout(self):
        self.set_x_expand(True)
        self.set_x_align(Clutter.ActorAlign.CENTER)
        self.set_y_expand(True)
        self.set_y_align(Clutter.ActorAlign.END)
        layout = Clutter.BoxLayout()
        layout.set_orientation(Clutter.Orientation.VERTICAL)
        layout.set_spacing(self.SPACING)
        self.set_layout_manager(layout)

    def _init_buttons(self):
        for i in range(9):
            button = buttons.FramedButtonType3()
            button.set_size(self.BT_WIDTH, self.BT_HEIGHT)
            self.add_child(button)
            button.set_model(self.BUTTONS[i])


class MenuCycle(switcher_app.Cycle):
    interval = 1000
    
    def __init__(self, actor):
        super().__init__()
        self.actor = actor
        self.STEPS = actor.get_children()
        self.index = 0
    
    def expose_next(self):
        self.STEPS[self.index-1].hilite_off()
        self.STEPS[self.index].hilite_on()
        self.index = (self.index + 1) % len(self.STEPS)

    def select(self):
        self.STEPS[self.index-1].select_on()
        return None
    
    def has_next(self):
        return True
        

class MainView(Clutter.Actor):
    """
    Speller main view containing all the elements.
    @param context switcher application context passed from application
    """
    ROW_SPACING = unit.mm(2)
    COL_SPACING = unit.mm(4)
    MARGIN = unit.mm(2)
    
    def __init__(self, context):
        super().__init__()
        self._init_layout()
        self._init_elements()

    def _init_layout(self):
        self.set_x_expand(True)
        self.set_y_expand(True)
        margin = Clutter.Margin()
        margin.top = margin.bottom = margin.left = margin.right = self.MARGIN
        self.set_margin(margin)
        self.layout = Clutter.GridLayout()
        self.layout.set_column_spacing(self.COL_SPACING)
        self.layout.set_row_spacing(self.ROW_SPACING)
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
        return KeyboardCycle(self.keyboard)


class MainViewCycle(switcher_app.Cycle):
    interval = 1000
    
    def __init__(self, actor):
        super().__init__()
        self.actor = actor
        self.STEPS = [
            actor.menu, actor.extra, actor.keyboard
            ]
        self.index = 0
    
    def expose_next(self):
        self.STEPS[self.index-1].hilite_off()
        self.STEPS[self.index].hilite_on()
        self.index = (self.index + 1) % 3
    
    def has_next(self):
        return True
    

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
