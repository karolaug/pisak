'''
Module with app-specific code for Digit Span game.
'''
from brain_flippers import launcher, score_manager
import os.path
from gi.repository import Mx

_INSTRUCTION_TEXT = \
    "W tej grze musisz zapamiętać wyświetlony na ekranie kod, a następnie " \
    "wpisać go na klawiaturze. Do punktacji liczy się liczba wpisanych " \
    "kodów oraz czas."

def prepare_menu_view(stage, script, data):
    GAME_TITLE = "Sejf"
    title = script.get_object("welcome_text")
    title.set_text(GAME_TITLE)
    stage.check_view = False

    game_button = script.get_object("start_button")
    game_button.connect("activate", lambda *_: stage.load_view("game", None))

    help_button = script.get_object("tutorial_button")
    help_button.connect("activate", lambda *_: stage.load_view("help", None))

    help_button = script.get_object("score_table_button")
    help_button.connect("activate", lambda *_: stage.load_view("top_list", False))


def prepare_game_view(stage, script, data):
    logic = script.get_object("logic")
    stage.check_view = True

    status_bar = script.get_object("status_bar")

    exit_button = status_bar.get_children()[2]
    exit_button.connect("activate", lambda *_: stage.load_view("menu", None))
    
    def show_results(*args):
        data = {"score": logic.score, "game": "digit_span"}
        if score_manager.is_top_ten("digit_span", logic.score):
            stage.load_view("result_top", data)
        else:
            stage.load_view("result_meh", data)
    
    logic.connect("finished", show_results)


def prepare_help_view(stage, script, data):
    instruction_text = script.get_object("text")
    instruction_text.set_text(_INSTRUCTION_TEXT)
    stage.check_view = True

    back_button = script.get_object("backButton")
    back_button.connect("activate", lambda *_: stage.load_view("menu", None))


def prepare_top_result_view(stage, script, data):
    def back_to_menu(*args):
        stage.load_view("menu", None)
    def show_top_list(*args):
        data = {"score": score_logic.game_score}
        stage.load_view("top_list", data)
    stage.check_view = True

    score_logic = script.get_object("logic")
    score_logic.game_score = data.get("score") 
    score_logic.game_name = "digit_span"
    keyboard_panel = script.get_object("keyboard_panel")
    score_logic.keyboard = keyboard_panel
    score_logic.connect("finished", back_to_menu)
    score_logic.connect("move-on", show_top_list)

def prepare_meh_result_view(stage, script, data):
    def back_to_menu(*args):
        stage.load_view("menu", None)

    stage.check_view = True
    score_logic = script.get_object("logic")
    score_logic.game_score = data.get("score")
    score_logic.game_name = "digit_span"
    score_logic.connect("finished", back_to_menu)


def prepare_top_list_view(stage, script, data):
    title_text = "Dzisiejsze wyniki:"
    def back_to_menu(*args):
        stage.load_view("menu", None)
    stage.check_view = True
    logic = script.get_object("logic")
    logic.game = "digit_span"
    if data == False:
        logic.only_today = False
        title_text = "WYNIKI Z KIEDYKOLWIEK:"
        
    else:
        logic.only_today = True
        title_text = "DZISIEJSZE WYNIKI:"
    logic.results_table = script.get_object("score_table")
    logic.best_score = script.get_object("best_score_value")
    script.get_object("title").set_text(title_text)
    exit_button = script.get_object("exit_button")
    exit_button.connect("activate", back_to_menu)
    logic.generate_results()


def fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)
  
DIGIT_SPAN_APP = {
    "views": {
        "menu": (fix_path("../menu_screen.json"), prepare_menu_view),
        "game": (fix_path("game_screen.json"), prepare_game_view),
        "help": (fix_path("tutorial.json"), prepare_help_view),
        "result_top": (fix_path("../player_success_screen.json"), prepare_top_result_view),
        "result_meh": (fix_path("../player_fail_screen.json"), prepare_meh_result_view),
        "top_list": (fix_path("../high_scores_screen.json"), prepare_top_list_view)
    },
    "initial-view": "menu",
    "initial-data": None,
    "background-color": "#006"
}


if __name__ == "__main__":
    launcher.run(DIGIT_SPAN_APP)
