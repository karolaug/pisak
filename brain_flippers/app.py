import sys
import os.path

from gi.repository import Clutter, Mx

from pisak import switcher_app
from brain_flippers import score_manager, widgets

import pisak.widgets  # @UnusedImport
import pisak.layout  # @UnusedImport
import brain_flippers.puzzle.master  # @UnusedImport

VIEW_PATHS = {
  "high_scores": "puzzle/high_scores_screen.json",
  "player_success": "puzzle/player_success_screen.json",
  "player_fail": "puzzle/player_fail_screen.json",
  "welcome_screen": "puzzle/welcome_screen.json",
  "game_screen": "main_game_screen.json"
}


class BrainPuzzleStage(Clutter.Stage):
    INITIAL_VIEW = "welcome_screen"

    def __init__(self, context):
        super().__init__()
        self._init_views()
        self.view_transition_duration = 400
        self.view_transition_delay = 1000
        black = Clutter.Color.new(0, 0, 0, 255)
        self.set_background_color(black)
        self.set_layout_manager(Clutter.BinLayout())
        self.context = context
        self.enter_welcome_view()

    def _init_views(self):
        current_path = os.path.split(__file__)[0]
        self.views = {}
        for name, path in VIEW_PATHS.items():
            if path is None:
                continue
            view_script = Clutter.Script()
            view_script.load_from_file(os.path.join(current_path, path))
            self.views[name] = view_script

    def resolve_path(self, path):
        current_path = os.path.split(__file__)[0]
        return os.path.join(current_path, path)

    def load_view_from_script(self, name):
        self.script = Clutter.Script()
        path = self.resolve_path(VIEW_PATHS[name])
        self.script.load_from_file(path)
        Clutter.threads_add_timeout(0, self.view_transition_delay, self.switch_views, None)

    def switch_views(self, *args):
        if self.get_children():
            self.remove_all_children()
        new_view = self.script.get_object("main")
        new_view.set_opacity(0)
        self.add_child(new_view)
        transition = Clutter.PropertyTransition.new("opacity")
        transition.set_to(255)
        transition.set_remove_on_complete(True)
        transition.set_duration(self.view_transition_duration)
        new_view.add_transition("opacity", transition)
        
    def enter_welcome_view(self, *args):
        self.load_view_from_script("welcome_screen")
        self.enable_welcome_view()

    def enable_welcome_view(self):
        start_button = self.script.get_object("start_button")
        start_button.connect("activate", self.enter_game_view)

    def enter_game_view(self, *args):
        self.load_view_from_script("game_screen")
        self.enable_game_view()

    def enable_game_view(self):
        game_actor = self.script.get_object("main")
        game_actor.connect("game-end", self.enter_player_result_view)
        
    def enter_player_result_view(self, game_outcome):
        score = game_outcome.player_points - game_outcome.player_errors
        db_records = score_manager.get_best_today("puzzle")
        if len(db_records) < 10 or score >= db_records[-1][1]:
            self.enter_player_success_view(game_outcome)
        else:
            self.enter_player_fail_view(game_outcome)
            
    def enter_player_success_view(self, game_outcome): 
        self.load_view_from_script("player_success")
        self.adjust_player_success_view(game_outcome)
        self.enable_player_success_view()

    def adjust_player_success_view(self, game_outcome):
        score_entry = self.script.get_object("score_value")
        score = game_outcome.player_points - game_outcome.player_errors
        score_entry.set_text(str(score))

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
        try_again_button.connect("activate", self.enter_game_view)
        best_today_button = self.script.get_object("best_today")
        best_today_button.connect("activate", self.enter_high_scores_view, "today")
        best_ever_button = self.script.get_object("best_ever")
        best_ever_button.connect("activate", self.enter_high_scores_view, "ever")
            
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
            name = "Gall Anonim"
        score = float(self.script.get_object("score_value").get_text())
        score_manager.add_record("puzzle", name, score)

    def enter_player_fail_view(self, game_outcome):
        self.load_view_from_script("player_fail")
        self.adjust_player_fail_view(game_outcome)
        self.enable_player_fail_view()

    def adjust_player_fail_view(self, game_outcome):
        player_score_entry = self.script.get_object("player_score_value")
        player_score = game_outcome.player_points - game_outcome.player_errors
        player_score_entry.set_text(str(player_score))
        average_score_entry = self.script.get_object("average_score_value")
        average_score = score_manager.get_average_ever("puzzle")
        average_score_entry.set_text(str(round(average_score, 2)))
        
    def enable_player_fail_view(self):
        try_again_button = self.script.get_object("try_again")
        try_again_button.connect("activate", self.enter_game_view)
        best_today_button = self.script.get_object("best_today")
        best_today_button.connect("activate", self.enter_high_scores_view, "today")
        best_ever_button = self.script.get_object("best_ever")
        best_ever_button.connect("activate", self.enter_high_scores_view, "ever")

    def enter_high_scores_view(self, source, request):
        self.load_view_from_script("high_scores")
        self.adjust_high_scores_view(request)
        self.enable_high_scores_view()

    def adjust_high_scores_view(self, request):
        if request == "today":
            db_records = score_manager.get_best_today("puzzle")
            self.script.get_object("title").set_text("WYNIKI Z DZIŚ")
        elif request == "ever":
            db_records = score_manager.get_best_ever("puzzle")
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
        exit_button.connect("activate", self.enter_welcome_view)

    
class BrainPuzzleApp(switcher_app.Application):
    """
    Brain flipper app with brain flipper stage.
    """
    def create_stage(self, argv):
        stage = BrainPuzzleStage(self.context)
        stage.set_fullscreen(True)
        return stage


if __name__ == "__main__":
    BrainPuzzleApp(sys.argv).main()
