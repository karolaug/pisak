'''
Test brainflippers' result logic
'''
import unittest
from gi.repository import Clutter
import brain_flippers.widgets
from brain_flippers.widgets import PuzzleButton


class TestResultLogic(unittest.TestCase):
    def setUp(self):
        Clutter.init([])
    
    def test_set_game_results(self):
        logic = brain_flippers.widgets.TopResultLogic()
        logic.game_name = "dummy_game"
        logic.game_score = 42
    
    def test_keyboard(self):
        logic = brain_flippers.widgets.TopResultLogic()
        keyboard = Clutter.Actor()
        button = PuzzleButton()
        button.set_label("A")
        keyboard.add_actor(button)
        logic.keyboard = keyboard
        button.emit("activate")
        self.assertEqual(logic.typed_player_name, "A")
    
    def test_player_name(self):
        logic = brain_flippers.widgets.TopResultLogic()
        player_name = Clutter.Text()
        logic.player_name = player_name

        self.assertEqual(player_name.get_text(), "_ _")

        logic.typed_player_name = "X"
        self.assertEqual(player_name.get_text(), "X _") 

        logic.typed_player_name = "XY"
        self.assertEqual(player_name.get_text(), "X Y")
    
    def test_score(self):
        logic = brain_flippers.widgets.TopResultLogic()
        player_score = Clutter.Text()
        score_1 = 42
        score_2 = 9001
        logic.game_score = score_1  # set value
        logic.player_score = player_score  # set text box
        self.assertEqual(str(score_1), player_score.get_text())
        logic.game_score = score_2  # set other value
        self.assertEqual(str(score_2), player_score.get_text())


if __name__ == "__main__":
    unittest.main()