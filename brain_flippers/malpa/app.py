'''
Module with app-specific code for Digit Span game.
'''
from brain_flippers import launcher, score_manager
import os.path

def prepare_menu_view(stage, script, data):
    GAME_TITLE = "Malpa"
    title = script.get_object("welcome_text")
    title.set_text(GAME_TITLE)
    
    game_button = script.get_object("start_button")
    game_button.connect("activate", lambda *_: stage.load_view("game", None))

    help_button = script.get_object("tutorial_button")
    help_button.connect("activate", lambda *_: stage.load_view("help", None))

def prepare_game_view(stage, script, data):
    logic = script.get_object("logic")
    
    def show_results(*args):
        data = {"score": logic.score, "game": "malpa"}
        if score_manager.is_top_ten("bomba", logic.score):
            stage.load_view("result_top", data)
        else:
            stage.load_view("result_meh", data)
    
    logic.connect("finished", show_results)


def prepare_help_view(stage, script, data):
    back_button = script.get_object("back_button")
    back_button.connect("clicked", lambda *_: stage.load_view("menu", None))
    
    movie = script.get_object("movie")
    movie.video_texture.set_playing(True)

def prepare_top_result_view(stage, script, data):
    def back_to_menu(*args):
        stage.load_view("menu", None)
    def show_top_list(*args):
        data = {"score": score_logic.game_score}
        stage.load_view("top_list", data)

    score_logic = script.get_object("logic")
    score_logic.game_score = data.get("score") 
    score_logic.game_name = "malpa"
    keyboard_panel = script.get_object("keyboard_panel")
    score_logic.keyboard = keyboard_panel
    score_logic.connect("finished", back_to_menu)
    score_logic.connect("move-on", show_top_list)

def prepare_meh_result_view(stage, script, data):
    score = data.get("score")
    score_message = str(score)
    message_label = script.get_object("player_score_value")
    message_label.set_text(score_message)

    button = script.get_object("try_again")
    button.connect("activate", lambda *_: stage.load_view("game", None))


def prepare_top_list_view(stage, script, data):
    title_text = "Dzisiejsze wyniki:"
    def back_to_menu(*args):
        stage.load_view("menu", None)
    logic = script.get_object("logic")
    logic.game = "malpa"
    logic.only_today = True
    logic.results_table = script.get_object("score_table")
    logic.best_score = script.get_object("best_score_value")
    script.get_object("title").set_text(title_text)
    exit_button = script.get_object("exit_button")
    exit_button.connect("activate", back_to_menu)
    logic.generate_results()

def fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)
  
MALPA_APP = {
    "views": {
        "menu": (fix_path("../menu_screen.json"), prepare_menu_view),
        "game": (fix_path("stage.json"), prepare_game_view),
        "help": (fix_path("movie.json"), prepare_help_view),
        "result_top": (fix_path("../player_success_screen.json"), prepare_top_result_view),
        "result_meh": (fix_path("../player_fail_screen.json"), prepare_meh_result_view),
        "top_list": (fix_path("../high_scores_screen.json"), prepare_top_list_view)
    },
    "initial-view": "menu",
    "initial-data": None,
    "background-color": "000000"
}


if __name__ == "__main__":
    launcher.run(MALPA_APP)
