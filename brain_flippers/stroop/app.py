"""
Main module of the stroop game application. The whole gui part of the game,
at least for now, is divided into three classes, that is: so called stage-
main class responsible for switching the main views and organizing communication
between them, with methods which names begin with enter- they introduce
new views, adjust- they make all the neccessary gui adjustments like setting
appropriate info messages, button labels etc and enable- they take buttons
or the whole views from dedicated jsons and connect signals to them;
game- class that runs the proper game, used as an object by the main game json,
switching colors and rules changed views by itself, counts time and points,
sends game end signal when the game is over; and finally tutorial- class
responsible for the whole tutorial part, used as an object by the main tutorial
json, switches between three views, sends the tutorial end signal when the tutorial is over.
All used parameters are declared at the beginning of the module or very close to
the beginning of a proper class.
"""

import sys
import os.path
import random

from gi.repository import Clutter, Mx, GObject

from pisak import switcher_app, unit
from brain_flippers import score_manager
from brain_flippers import widgets

import pisak.layout  # @UnusedImport

WELCOME_TEXT = "WITAJ W GRZE STROOP"
INDEX_FINGER_ICON_PATH = "brain_flippers/stroop/index_finger.png"
PLAYER_LIFE_UNICHAR = u"\u2764"
VIEW_PATHS = {
    "game": "brain_flippers/stroop/main_game_screen.json",
    "colors": "brain_flippers/stroop/colors_screen.json",
    "rules_changed": "brain_flippers/stroop/rules_changed_screen.json",
    "main_menu": "brain_flippers/menu_screen.json",
    "high_scores": "brain_flippers/high_scores_screen.json",
    "player_success": "brain_flippers/player_success_screen.json",
    "player_fail": "brain_flippers/player_fail_screen.json",
    "tutorial": "brain_flippers/stroop/main_tutorial_screen.json",
    "tutorial_colors": "brain_flippers/stroop/tutorial_colors_screen.json"
}
COLORS_MAP = {
    "czerwony": Clutter.Color.from_string("#FF0000")[1],
    "żółty": Clutter.Color.from_string("#FFFF00")[1],
    "zielony": Clutter.Color.from_string("#00FF00")[1],
    "niebieski": Clutter.Color.from_string("#0000FF")[1]
}
RULES_CHANGED_TEXT = {
    "0": "UWAGA! ZMIANA REGUŁ GRY!\n"
         "REAGUJ NA NA KOLOR SŁÓW\n"
         "WYBIERAJĄC ODPOWIEDNIE POLA.\n"
         "IGNORUJ ICH ZNACZENIE.",
    "1": "UWAGA! ZMIANA REGUŁ GRY!\n"
         "REAGUJ NA NA ZNACZENIE SŁÓW\n"
         "WYBIERAJĄC ODPOWIEDNIE POLA.\n"
         "IGNORUJ ICH KOLOR."
}
TUTORIAL_TEXT = {
    "0": "W PIERWSZEJ CZĘŚCI GRY BĘDZIESZ MUSIAŁ REAGOWAĆ\n"
         "NA KOLORY. W TYM PRZYKŁADZIE NA EKRANIE WIDZISZ\n"
         """SŁOWO "ŻÓŁTY" NAPISANE NA CZERWONO.""",
    "1": "IGNORUJ TREŚĆ SŁOWA I JAK NAJSZYBCIEJ WYBIERZ POLE\n"
         "ODPOWIADAJĄCE KOLOROWI LITER, CZYLI W TYM PRZYPADKU\n"
         "CZERWONE. W TEN SPOSÓB ZDOBĘDZIESZ PUNKT.",
    "2": """TERAZ WIDZIMY SŁOWO "CZERWONY" NAPISANE ZIELONYMI\n"""
         "LITERAMI, WIĘC JAK NAJSZYBCIEJ WYBIERAMY ZIELONE POLE\n"
         "I ZDOBYWAMY DRUGI PUNKT..."
}

class BrainStroopGame(Clutter.Actor):
    __gtype_name__ = "BrainStroopGame"
    __gsignals__ = {
        "game_end": (GObject.SIGNAL_RUN_FIRST, None, ()),
        "game_over": (GObject.SIGNAL_RUN_FIRST, None, ()),
    }
    
    def __init__(self):
        super().__init__()
        self.set_layout_manager(Clutter.BinLayout())
        self._init_parameters()
        self.enter_colors_view()

    def _init_parameters(self):
        self.level = 0
        self.mode = 0
        self.lap = 0
        self.levels = 1
        self.color_repetition = 2
        self.laps_per_mode = self.color_repetition * len(COLORS_MAP)
        self.player_score = 0
        self.player_clock = 0
        self.player_correct_answers = 0
        self.player_errors = 0
        self.player_clock_quantum = 1000
        self.player_clock_ticking = False
        self.player_score_coeff = 10
        self.player_lives = 4
        self.player_lives_left = self.player_lives
        self.rules_changed_view_idle = 2000

    def _load_view_from_script(self, name):
        self.script = Clutter.Script()
        path = VIEW_PATHS[name]
        self.script.load_from_file(path)
        if self.get_children():
            self.remove_all_children()
        view_actor = self.script.get_object("main")
        self.add_child(view_actor)

    def enter_colors_view(self, *args):
        self._load_view_from_script("colors")
        self.color_values_chain = self.color_repetition * list(COLORS_MAP.values())
        self.color_names_chain = self.color_repetition * list(COLORS_MAP.keys())
        random.shuffle(self.color_values_chain)
        random.shuffle(self.color_names_chain)
        self.display_player_life_panel()
        self.adjust_colors_view()
        self.enable_color_view()
        self.player_clock_ticking = True
        Clutter.threads_add_timeout(0, self.player_clock_quantum, self.update_player_clock, None)

    def adjust_colors_view(self):
        color_text_entry = self.script.get_object("color_text")
        color_text_entry.set_text(self.color_names_chain.pop(0))
        color_text_entry.set_color(self.color_values_chain.pop(0))

    def enable_color_view(self):
        for field in self.script.get_object("color_fields").get_children():
            field.connect("button-press-event", self.on_player_choice)
            field.connect("touch-event", self.on_player_choice)
            field.set_reactive(True)

    def update_player_clock(self, *args):
        self.player_clock += 1
        if self.player_clock_ticking:
            return True
        else:
            return False
        
    def display_player_life_panel(self):
        life_panel = self.script.get_object("life_panel")
        for life in range(self.player_lives_left):
            life_panel.insert_unichar(PLAYER_LIFE_UNICHAR)

    def enter_rules_changed_view(self):
        self.player_clock_ticking = False
        self._load_view_from_script("rules_changed")
        self.adjust_rules_changed_view()
        self.enable_rules_changed_view()

    def adjust_rules_changed_view(self):
        self.script.get_object("info_text").set_text(RULES_CHANGED_TEXT[str(self.mode)])

    def enable_rules_changed_view(self):
        start_button = self.script.get_object("start_button")
        start_button.connect("activate", self.enter_colors_view)

    def on_player_choice(self, field, event):
        if isinstance(event, Clutter.TouchEvent):
            if event.type != 13:  # touch-begin type of event
                return
        self.lap += 1
        field_color = field.get_background_color()
        if self.mode == 0:
            requested_color = self.script.get_object("color_text").get_color()
        elif self.mode == 1:
            requested_color = COLORS_MAP[self.script.get_object("color_text").get_text()]
        if Clutter.Color.equal(field_color, requested_color):
            self.on_correct_answer()
        else:
            self.on_life_loss()

    def on_correct_answer(self):
        self.player_correct_answers += 1
        self.move_on()
        
    def on_life_loss(self):
        self.player_errors += 1
        self.player_lives_left -= 1
        life_panel = self.script.get_object("life_panel")
        life_panel.set_text(life_panel.get_text()[:-1])
        if not self.player_lives_left:
            self.end_game()
        else:
            self.move_on()

    def move_on(self):
        if self.lap == self.laps_per_mode:
            self.lap = 0
            if self.mode == 0:
                self.mode = 1
            elif self.mode == 1:
                self.mode = 0
                self.level += 1
                if self.level == self.levels:
                    self.end_game()
                    return
            self.enter_rules_changed_view()
        elif self.lap < self.laps_per_mode:
            self.adjust_colors_view()
                        
    def end_game(self):
        self.calculate_player_score()
        self.emit("game_end")

    def calculate_player_score(self):
        self.player_score = self.player_score_coeff * self.player_correct_answers / (1+self.player_errors) / (1+self.player_clock)
            

class BrainStroopTutorial(Clutter.Actor):
    __gtype_name__ = "BrainStroopTutorial"
    __gsignals__ = {
        "tutorial_end": (GObject.SIGNAL_RUN_FIRST, None, ())
    }
    
    def __init__(self):
        super().__init__()
        self.set_layout_manager(Clutter.BinLayout())
        self._init_parameters()
        self._load_script()
        self._init_index_finger()
        self.reload_view()

    def _load_script(self):
        self.script = Clutter.Script()
        self.script.load_from_file(VIEW_PATHS["tutorial_colors"])
        view_actor = self.script.get_object("main")
        self.add_child(view_actor)

    def _init_parameters(self):
        self.index_finger_width = 100
        self.index_finger_height = 120
        self.view_num = 0
        self.views = 3

    def _init_index_finger(self):
        self.index_finger = Mx.Image()
        self.index_finger.set_from_file(INDEX_FINGER_ICON_PATH)
        self.index_finger.set_scale_mode(1)  # fit scale mode
        self.index_finger.set_size(self.index_finger_width, self.index_finger_height)

    def reload_view(self):
        self.enable_view()
        self.adjust_view()

    def adjust_view(self):
        info_text = self.script.get_object("info_text")
        info_text.set_text(TUTORIAL_TEXT[str(self.view_num)])
        if self.view_num == 0:
            color_text = self.script.get_object("color_text")
            color_text.set_color(COLORS_MAP["czerwony"])
            color_text.set_text("żółty")
            next_button = self.script.get_object("next_button")
            next_button.set_label("DALEJ")
        elif self.view_num == 1:
            self.allocate_index_finger(self.script.get_object("red"))
            next_button = self.script.get_object("next_button")
            next_button.set_label("DALEJ")
        elif self.view_num == 2:
            self.script.get_object("red").remove_child(self.index_finger)
            self.allocate_index_finger(self.script.get_object("green"))
            color_text = self.script.get_object("color_text")
            color_text.set_color(COLORS_MAP["zielony"])
            color_text.set_text("czerwony")
            next_button = self.script.get_object("next_button")
            next_button.set_label("WYJDŹ")
            
    def enable_view(self):
        next_button = self.script.get_object("next_button")
        if self.view_num == 0:
            next_button.connect("activate", self.next_page)
        elif self.view_num == 2:
            next_button.disconnect_by_func(self.next_page)
            next_button.connect("activate", self.end_tutorial)

    def allocate_index_finger(self, relative_field):
        self.index_finger.clear_constraints()
        relative_field.set_layout_manager(Clutter.BinLayout())
        relative_field.add_child(self.index_finger)
        relative_y = relative_field.get_height()/3
        bind_y = Clutter.BindConstraint.new(relative_field, Clutter.BindCoordinate.Y, relative_y)
        self.index_finger.add_constraint(bind_y)

    def end_tutorial(self, *args):
        self.emit("tutorial-end")

    def next_page(self, *args):
        self.view_num = self.view_num + 1
        self.reload_view()
        

class BrainStroopStage(Clutter.Stage):
    def __init__(self, context):
        super().__init__()
        self.set_layout_manager(Clutter.BinLayout())
        black = Clutter.Color.new(0, 0, 0, 255)
        self.set_background_color(black)
        self.db_max_len = 10
        self.enter_initial_view()

    def _load_view_from_script(self, name):
        self.script = Clutter.Script()
        path = VIEW_PATHS[name]
        self.script.load_from_file(path)
        if self.get_children():
            self.remove_all_children()
        view_actor = self.script.get_object("main")
        self.add_child(view_actor)

    def enter_initial_view(self):
        self.enter_main_menu_view()

    def enter_main_menu_view(self, *args):
        self._load_view_from_script("main_menu")
        self.adjust_main_menu_view()
        self.enable_main_menu_view()

    def adjust_main_menu_view(self):
        welcome_text = self.script.get_object("welcome_text")
        welcome_text.set_text(WELCOME_TEXT)
        high_scores = score_manager.get_best_ever("stroop")
        if not high_scores:
            self.script.get_object("score_table_button").hide()

    def enable_main_menu_view(self):
        start_button = self.script.get_object("start_button")
        start_button.connect("activate", self.enter_game_view)
        tutorial_button = self.script.get_object("tutorial_button")
        tutorial_button.connect("activate", self.enter_tutorial_view)
        high_scores_button = self.script.get_object("score_table_button")
        high_scores_button.connect("activate", self.enter_high_scores_view, "ever")

    def enter_tutorial_view(self, *args):
        self._load_view_from_script("tutorial")
        self.enable_tutorial_view()

    def enable_tutorial_view(self):
        tutorial_actor = self.script.get_object("main")
        tutorial_actor.connect("tutorial-end", self.enter_main_menu_view)

    def enter_game_view(self, *args):
        self._load_view_from_script("game")
        self.enable_game_view()

    def enable_game_view(self):
        game_actor = self.script.get_object("main")
        game_actor.connect("game-end", self.enter_player_result_view)

    def enter_player_result_view(self, game_outcome):
        score = game_outcome.player_score
        db_records = score_manager.get_best_today("stroop")
        if db_records:
            if len(db_records) < self.db_max_len or score >= db_records[-1][1]:
                self.enter_player_success_view(game_outcome)
            else:
                self.enter_player_fail_view(game_outcome)
        else:
            self.enter_player_success_view(game_outcome)
            
    def enter_player_success_view(self, game_outcome): 
        self._load_view_from_script("player_success")
        self.adjust_player_success_view(game_outcome)
        self.enable_player_success_view()

    def adjust_player_success_view(self, game_outcome):
        score_entry = self.script.get_object("player_score_value")
        score = round(game_outcome.player_score, 2)
        score_entry.set_text(str(score))
        average_score = score_manager.get_average_ever("stroop")
        if average_score:
            average_score_entry = self.script.get_object("average_score_value")
            average_score_entry.set_text(str(round(average_score, 2)))
        else:
            self.script.get_object("average_score").hide()

    def enable_player_success_view(self):
        for item in self.script.list_objects():
            if isinstance(item, widgets.PuzzleButton):
                if len(item.label) == 1 and item.label.isalpha():
                    item.connect("activate", self.type_name)
                elif item.label == "SKASUJ":
                    item.connect("activate", self.delete_name_char)
                elif item.label == "ZAPISZ":
                    item.connect("activate", self.save_score)
                    item.connect_after("activate", self.enter_high_scores_view, "today")
        try_again_button = self.script.get_object("try_again")
        try_again_button.connect("activate", self.enter_main_menu_view)
        best_today_button = self.script.get_object("best_today")
        if score_manager.get_best_today("stroop"):
            best_today_button.connect("activate", self.enter_high_scores_view, "today")
        else:
            best_today_button.hide()
        best_ever_button = self.script.get_object("best_ever")
        if score_manager.get_best_ever("stroop"):
            best_ever_button.connect("activate", self.enter_high_scores_view, "ever")
        else:
            best_ever_button.hide()
            
    def type_name(self, button):
        name_entry = self.script.get_object("name")
        name = name_entry.get_text()
        if "_" in name:
            letter = button.label
            name_entry.set_text(name.replace("_", letter, 1))

    def delete_name_char(self, *args):
        name_entry = self.script.get_object("name")
        name = name_entry.get_text()
        if name.count("_") == 0:
            name = name[:-1] + "_"
        elif name.count("_") == 1:
            name = "_" + name[1:]
        name_entry.set_text(name)

    def save_score(self, *args):
        name = self.script.get_object("name").get_text()
        if "_" in name:
            name = "NN"
        else:
            name = name.replace(" ", "")
        score = float(self.script.get_object("player_score_value").get_text())
        score_manager.add_record("stroop", name, score)

    def enter_player_fail_view(self, game_outcome):
        self._load_view_from_script("player_fail")
        self.adjust_player_fail_view(game_outcome)
        self.enable_player_fail_view()

    def adjust_player_fail_view(self, game_outcome):
        player_score_entry = self.script.get_object("player_score_value")
        player_score = round(game_outcome.player_score, 2)
        player_score_entry.set_text(str(player_score))
        average_score = score_manager.get_average_ever("stroop")
        if average_score:
            average_score_entry = self.script.get_object("average_score_value")
            average_score_entry.set_text(str(round(average_score, 2)))
        else:
            self.script.get_object("average_score").hide()
        
    def enable_player_fail_view(self):
        try_again_button = self.script.get_object("try_again")
        try_again_button.connect("activate", self.enter_main_menu_view)
        best_today_button = self.script.get_object("best_today")
        best_today_button.connect("activate", self.enter_high_scores_view, "today")
        best_ever_button = self.script.get_object("best_ever")
        best_ever_button.connect("activate", self.enter_high_scores_view, "ever")

    def enter_high_scores_view(self, source, request):
        self._load_view_from_script("high_scores")
        self.adjust_high_scores_view(request)
        self.enable_high_scores_view()

    def adjust_high_scores_view(self, request):
        if request == "today":
            db_records = score_manager.get_best_today("stroop")
            self.script.get_object("title").set_text("WYNIKI Z DZIŚ")
        elif request == "ever":
            db_records = score_manager.get_best_ever("stroop")
            self.script.get_object("title").set_text("WYNIKI Z KIEDYKOLWIEK")
        best_score_entry = self.script.get_object("best_score_value")
        best_score_entry.set_text(str(db_records[0][1]))
        score_table = self.script.get_object("score_table")
        for idx, row in enumerate(score_table.get_children()):
            name_entry = row.get_children()[1]
            score_entry = row.get_children()[2]
            if idx < len(db_records):
                name_entry.set_text(db_records[idx][0])
                score_entry.set_text(str(db_records[idx][1]))
            else:
                row.hide()

    def enable_high_scores_view(self):
        exit_button = self.script.get_object("exit_button")
        exit_button.connect("activate", self.enter_main_menu_view)
    

class BrainStroopApp(switcher_app.Application):
    """
    Brain stroop app with brain stroop stage.
    """
    def create_stage(self, argv):
        stage = BrainStroopStage(self.context)
        stage.set_size(unit.size_pix[0], unit.size_pix[1])
        stage.set_fullscreen(True)
        return stage

if __name__ == "__main__":
    BrainStroopApp(sys.argv).main()
