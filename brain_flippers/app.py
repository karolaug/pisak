import sys
import os.path

from gi.repository import Clutter, Mx

from pisak import switcher_app
from pisak import signals
from brain_flippers import score_manager

import pisak.widgets  # @UnusedImport
import pisak.layout  # @UnusedImport
import brain_flippers.puzzle.master  # @UnusedImport

VIEW_PATHS = {
  "high_scores": "puzzle/best_result_screen.json",
  "player_score": "puzzle/user_result_screen.json",
  "welcome_screen": "puzzle/welcome_screen.json",
  "game_screen": "main_game_screen.json"
}


class BrainPuzzleStage(Clutter.Stage):
    INITIAL_VIEW = "welcome_screen"

    def __init__(self, context):
        super().__init__()
        self._init_views()
        self.context = context

    def _init_views(self):
        current_path = os.path.split(__file__)[0]
        self.views = {}
        for name, path in VIEW_PATHS.items():
            if path is None:
                continue
            view_script = Clutter.Script()
            view_script.load_from_file(os.path.join(current_path, path))
            self.views[name] = view_script
        self.enter_welcome_view()

    def enter_welcome_view(self, *args):
        if self.get_children():
            self.remove_all_children()
        self.script = self.views[self.INITIAL_VIEW]
        view_actor = self.script.get_object("main")
        self.set_layout_manager(Clutter.BinLayout())
        self.add_child(view_actor)
        start_button = self.script.get_object("start_button")
        start_button.connect("clicked", self.enter_game_view)

    def enter_game_view(self, *args):
        if self.get_children():
            self.remove_all_children()
        self.script = self.views["game_screen"]
        view_actor = self.script.get_object("main")
        self.add_child(view_actor)
        view_actor.connect("leave", self.enter_user_result_view, view_actor)
        
    def enter_user_result_view(self, source, game_outcome):
        if self.get_children():
            self.remove_all_children()
        self.script = self.views["player_score"]
        view_actor = self.script.get_object("main")
        self.add_child(view_actor)
        score_field = self.script.get_object("score_value")
        score = game_outcome.player_points - game_outcome.player_errors
        score_field.set_text(str(score))
        for item in self.script.list_objects():
            if isinstance(item, Mx.Button):
                if len(item.get_label()) == 1:
                    item.connect("clicked", self.type_name)
                elif item.get_label() == "SKASUJ":
                    item.connect("clicked", self.delete_name_char)
                elif item.get_label() == "ZAPISZ":
                    item.connect("clicked", self.save_score)
        try_again_button = self.script.get_object("try_again")
        try_again_button.connect("clicked", lambda *_: self._init_views())
        best_today_button = self.script.get_object("best_today")
        best_today_button.connect("clicked", self.enter_best_result_view, "today")
        best_ever_button = self.script.get_object("best_ever")
        best_ever_button.connect("clicked", self.enter_best_result_view, "ever")
            
    def type_name(self, source):
        name_field = self.script.get_object("name")
        name = name_field.get_text()
        if "_" in name:
            letter = source.get_label()
            name_field.set_text(name.replace("_", letter, 1))

    def delete_name_char(self, source):
        name_field = self.script.get_object("name")
        name = name_field.get_text()
        if name.count("_") == 0:
            name = name[:-1] + "_"
        elif name.count("_") == 1:
            name = "_" + name[1:]
        name_field.set_text(name)

    def save_score(self, source):
        name = self.script.get_object("name").get_text()
        if "_" in name:
            name = "Gall Anonim"
        score = float(self.script.get_object("score_value").get_text())
        score_manager.add_record("puzzle", name, score)
        self.enter_best_result_view("today")

    def enter_best_result_view(self, *args):
        if self.get_children():
            self.remove_all_children()
        self.script = self.views["high_scores"]
        view_actor = self.script.get_object("main")
        self.add_child(view_actor)
        exit_button = self.script.get_object("exit_button")
        exit_button.connect("clicked", lambda *_: self._init_views())
        score_table = self.script.get_object("score_table")
        if "today" in args:
            db_records = score_manager.get_best_today("puzzle")
            self.script.get_object("title").set_text("WYNIKI Z DZIŚ")
        elif "ever" in args:
            db_records = score_manager.get_best_ever("puzzle")
            self.script.get_object("title").set_text("WYNIKI Z KIEDYKOLWIEK")
        for idx, row in enumerate(score_table.get_children()):
            name_field = row.get_children()[1]
            score_field = row.get_children()[2]
            if idx < len(db_records):
                name_field.set_text(db_records[idx][0])
                score_field.set_text(str(db_records[idx][1]))
            else:
                row.hide()
	
    
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
