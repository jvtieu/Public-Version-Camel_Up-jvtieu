import os, sys
import io
import contextlib
import unittest
from unittest.mock import patch
from colorama import Fore, Back, Style, init

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

Player = None
if not Player:
    from Player import Player as Player 

CamelUp = None
if not CamelUp:
    from CamelUp import CamelUp as CamelUp 

class Test_CamelUp(unittest.TestCase):
    def setUp(self):
        """runs before each test"""
        self.camel_styles= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
        }
        self.game = CamelUp(self.camel_styles, [Player("Dave", self.camel_styles), Player("Sasha", self.camel_styles)])
    
    def test_camelup_data_attributes(self):
        """CamelUp- Data Types"""
        self.assertIsInstance(self.game.board, object, "CamelUp.board should return an object")
        self.assertIsInstance(self.game.players, list, "CamelUp.players should return a list")
        self.assertIsInstance(self.game.players[0], object, "CamelUp.players[0] should return an object")
        self.assertIsInstance(self.game.STYLES, dict, "CamelUp.STYLES should return a dict")
        self.assertEqual(self.game.STYLES, self.camel_styles, "CamelUp.STYLES should be a dict of the camel styles")
        first, second = self.game.process_leg_payouts()
        self.assertIn(first, self.camel_styles.keys(), "process_leg_payouts should return a valid camel color for first place")
        self.assertIn(second, self.camel_styles.keys(), "process_leg_payouts should return a valid camel color for second place")
    
    def test_camelup_process_leg_payouts_with_bets(self):
        """CamelUp- process_leg_payouts with player bets"""
        self.game.board.track[0][4] = 'y'
        self.game.board.track[0][3] = 'b'
        self.game.players[0].add_bet(('y', 5))
        self.game.players[0].add_bet(('b', 3))
        self.game.players[1].add_bet(('g', 2))
        self.game.players[1].add_bet(('r', 3))
        self.game.players[1].add_bet(('b', 5))
        self.assertEqual(self.game.players[0].money, 3, "Player.money should start at 3")
        self.assertEqual(self.game.players[1].money, 3, "Player.money should start at 3")
        first, second = self.game.process_leg_payouts()
        self.assertEqual(first, 'y', "process_leg_payouts should return the top camel on space 0 as first place")
        self.assertEqual(second, 'b', "process_leg_payouts should return the top camel on space 0 as first place")
        self.assertEqual(self.game.players[0].money, 9, "Player.money should increase by the value of the ticket for first place and second place bets")
        self.assertEqual(self.game.players[1].money, 2, "Player.money should increase by the value of the ticket for first place and second place bets")


    def test_camelup_process_leg_payouts_with_no_bets(self):
        """CamelUp- process_leg_payouts with player bets"""
        first, second = self.game.process_leg_payouts()
        self.assertEqual(first, self.game.board.track[0][4], "process_leg_payouts should return the top camel on space 0 as first place")
        self.assertEqual(second, self.game.board.track[0][3], "process_leg_payouts should return the top camel on space 0 as first place")

        self.assertEqual(self.game.players[0].money, 3, "Player.money should start at 3") #no bets
        self.assertEqual(self.game.players[1].money, 3, "Player.money should start at 3") #no bets
    
    def test_camelup_play_leg_roll_red_die(self):
        """CamelUp- play_leg 'r' (roll) case rolls die, moves camel, and pays player $1"""
        self.game = CamelUp(self.camel_styles, [Player("Dave", self.camel_styles), Player("Sasha", self.camel_styles)])
        player = self.game.players[0]
        starting_money = player.money

        with patch.object(self.game, 'get_player_move', side_effect=['r']), \
            patch.object(self.game.board, 'is_leg_finished', side_effect=[False, True]), \
            patch.object(self.game.board, 'roll_die', return_value=('r', 2)) as mock_roll, \
            contextlib.redirect_stdout(io.StringIO()):

            self.game.play_leg()

            mock_roll.assert_called_once()

        self.assertEqual(player.money, starting_money + 1, "Players should gain $1 when rolling")
        self.assertIn("r",self.game.board.track[2], "Camels should move when die is rolled")
        self.assertNotIn("r", self.game.board.track[0], "Camels should move when die is rolled")
    
    def test_camelup_play_leg_roll_random_die(self):
        """CamelUp- play_leg rolls die and adds die to dice tents"""
        self.game = CamelUp(self.camel_styles, [Player("Dave", self.camel_styles), Player("Sasha", self.camel_styles)])

        with patch.object(self.game, 'get_player_move', side_effect=['r']), \
            patch.object(self.game.board, 'is_leg_finished', side_effect=[False, True]), \
            contextlib.redirect_stdout(io.StringIO()):
            self.game.play_leg()

        self.assertEqual(len(self.game.board.dice_tents), 1, "One die should be added to dice tents after rolling")
        added_die = self.game.board.dice_tents[0]
        # Check the data type: should be a tuple of (str, number)
        self.assertIsInstance(added_die, tuple, "Each entry in dice_tents should be a tuple")
        self.assertEqual(len(added_die), 2, "Each die tuple should have exactly 2 elements")
        self.assertIsInstance(added_die[0], str, "The first element of the die tuple should be a string (camel color)")
        self.assertIsInstance(added_die[1], (int, float), "The second element of the die tuple should be a number (die value)")
        # Check the values are sensible
        self.assertIn(added_die[0], self.camel_styles.keys(), "Rolled die color should be a valid camel color")
        # Check that die is removed from pyramid
        self.assertNotIn(added_die[0],self.game.board.pyramid.remaining_dice, "Rolled die should be removed from the dice pyramid")
    
    def test_camelup_play_leg_bet(self):
        """CamelUp- play_leg choice 'b', player bets on yellow camel"""
        self.game = CamelUp(self.camel_styles, [Player("Dave", self.camel_styles), Player("Sasha", self.camel_styles)])
        player = self.game.players[0]

        with patch.object(self.game, 'get_player_move', side_effect=['b']), \
            patch.object(self.game, 'get_player_bet', return_value='y'), \
            patch.object(self.game.board, 'is_leg_finished', side_effect=[False, True]), \
            contextlib.redirect_stdout(io.StringIO()):

            self.game.play_leg()
        self.assertIn(('y', 5), player.bets, "Player's bets should add the ticket they selected")
        self.assertEqual([3, 2, 2], self.game.board.ticket_tents['y'], "Top ticket should be removed from the ticket tent")

if __name__ == "__main__":
    unittest.main()
