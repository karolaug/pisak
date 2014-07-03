'''
Module with app-specific code for Digit Span game.
'''
from brain_flippers import launcher
import os.path

def prepare_menu_view(stage, script, data):
    GAME_TITLE = "Malpa"
    title = script.get_object("welcome_text")
    title.set_text(GAME_TITLE)
    
    game_button = script.get_object("start_button")
    game_button.connect("activate", lambda *_: stage.load_view("game", None))


def prepare_game_view(stage, script, data):
    logic = script.get_object("logic")
    
    def show_results(*args):
        data = {"score": logic.score, "game": "malpa"}
        
        stage.load_view("result", data)
    
    logic.connect("finished", show_results)


def prepare_help_view(script, data):
    pass


def prepare_result_view(stage, script, data):
    score = data.get("score")
    score_message = "Twój wynik to {}\n Gratulacje!".format(score)
    message_label = script.get_object("consolation")
    message_label.set_text(score_message)


def prepare_top_list_view(script, data):
    pass


def fix_path(path):
    return os.path.join(os.path.split(__file__)[0], path)
  
MALPA_APP = {
    "views": {
        "menu": (fix_path("../menu_screen.json"), prepare_menu_view),
        "game": (fix_path("stage.json"), prepare_game_view),
        "help": ("/dev/null", prepare_help_view),
        "result": ("../player_death_screen.json", prepare_result_view),
        "top_list": ("/dev/null", prepare_top_list_view)
    },
    "initial-view": "menu",
    "initial-data": None,
    "background-color": "000000"
}


if __name__ == "__main__":
    launcher.run(MALPA_APP)
