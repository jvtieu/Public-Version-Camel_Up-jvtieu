from colorama import Fore, Back, Style, init
from copy import deepcopy
from itertools import permutations, product
import math

try:
    from Board import Board
except ModuleNotFoundError:
    print("Board.py is not found.")
    pass

class AI:
    def __init__(self, board:Board):
        self.STYLES = board.STYLES
        self.board = board #reference to actual game board... updates as game is played
        pass

    def run_experimental_analysis(self, trials:int) -> dict[str, tuple[float, float]]:
        '''Conducts an experimental analysis (ie. a random simulation) of the probability that each camel
            will win either 1st or 2nd place in this leg of the race. The experimental analysis counts
            1st/2nd place finishes by counting outcomes from randomly shaking the pyramid over a given
            number of trials.

           General Steps:
                1) Save current gamestate using deepcopy
                2) Shake the pyramid and move camels enough times to finish the leg
                2) Count a 1st/2nd place finish for each camel
                3) Reset gamestate and repeat steps #1 - #2 trials number of times
                3) Calculate the probability that each camel will come in 1st or 2nd based on the total
                   number of 1st/2nd finishes out of the total number of trials

           Args
              trials (int): The number of random simulations to conduct

           Returns:
              dict[str, tuple[float, float]] - A dictionary representing the probabilities that a camel will
                                               come in first or second place according to an experimental analysis
                {
                    'r':(0.5, 0.2),
                    'b':(0.1, 0.04),
                    ...
                }
        '''
        camel_placements = {"r": [0,0], "g": [0,0], "b": [0,0], "p": [0,0], "y": [0,0]}
        for i in range(trials):
            copy_of_current_board = deepcopy(self.board)
            copy_of_remaining_dice = (5 - len(copy_of_current_board.dice_tents))
            for k in range (copy_of_remaining_dice):
                rolls = copy_of_current_board.roll_die()
                copy_of_current_board.move_camel(rolls)
            placement = copy_of_current_board.get_rankings()
            camel_placements[placement[0]][0] +=1
            camel_placements[placement[1]][1] +=1
        # red_win = (camel_placements["r"][0]/trial, camel_placements["r"][1]/trial)
        # green_win = (camel_placements["g"][0]/trial, camel_placements["g"][1]/trial)
        # blue_win = (camel_placements["b"][0]/trial, camel_placements["b"][1]/trial)
        # pink_win = (camel_placements["p"][0]/trial, camel_placements["p"][1]/trial)
        # yellow_win = (camel_placements["y"][0]/trial, camel_placements["y"][1]/trial)
        final_camel_placements = {"r": (camel_placements["r"][0]/trials, camel_placements["r"][1]/trials),
                                  "g": (camel_placements["g"][0]/trials, camel_placements["g"][1]/trials),
                                  "b": (camel_placements["b"][0]/trials, camel_placements["b"][1]/trials),
                                  "y": (camel_placements["y"][0]/trials, camel_placements["y"][1]/trials),
                                  "p": (camel_placements["p"][0]/trials, camel_placements["p"][1]/trials)}

        return final_camel_placements
                
            
        pass

    def get_ticket_EV(self, ticket_value:int, prob_first:float, prob_second:float)->float:
        '''Caclulates the Expected Value of a ticket

            Args:
                ticket_value (int): The value of a betting ticket if a camel comes in first place for a leg
                prob_first (float): The probability (0.0 - 1.0) that a camel will come in first place
                prob_second (float): The probability (0.0 - 1.0) that a camel will come in second place

            Return:
                float: The expected value of the ticket
        '''
        ev=0
        other=prob_first+prob_second
        place_1= prob_first*ticket_value
        place_2=prob_second
        place_other=(1-other)*-1
        ev=place_1+place_2+place_other
        return ev

        pass

    def __str__(self) -> str:
        exper = self.run_experimental_analysis(10000)

        stats_str=" Experimental\n"
        analysis = [(self.STYLES[c]+c+Style.RESET_ALL, exper[c][0], exper[c][1])  for c in exper ]
        stats_str+="   1st   2nd\n"
        for row in analysis:
            stats_str+="{: >1} {: >5.2f} {: >5.2f}".format(*row)+"\n"

        advice_str="Available bets: "
        best_ev = -10
        best_camel = "x"
        for color in self.board.ticket_tents:
            tickets_left = self.board.ticket_tents[color]
            if len(tickets_left) > 0:
                top_ticket_value=tickets_left[0]
                ev = self.get_ticket_EV(top_ticket_value, exper[color][0], exper[color][1])
                if ev>best_ev:
                    best_ev=ev
                    best_camel=color
                advice_str += f"({color})"+self.STYLES[color]+str(top_ticket_value)+Style.RESET_ALL+f" EV:{ev:.2f} "
            else:
                advice_str += f"({color})"+self.STYLES[color]+"X"+Style.RESET_ALL+" "

        advice_str += "\nAI Advice: "
        if best_ev>1:
            advice_str+=f"  Bet on {self.STYLES[best_camel]+best_camel+Style.RESET_ALL} with an expected value of {best_ev:.2f}\n"
        else:
            advice_str+="  No camel has an EV > 1. You should roll instead of bet.\n"

        return stats_str + advice_str

if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    game_board = Board(STYLES)
    ai = AI(game_board)
    print(game_board)
    # for _ in range(3):
    #     rolled_die=game_board.roll_die()
    #     game_board.move_camel(rolled_die)
    print(game_board)
    print(ai)
    print(game_board) #game state hasn't changed
