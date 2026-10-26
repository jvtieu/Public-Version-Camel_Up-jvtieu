import random
from colorama import Fore, Back, Style, init

class Pyramid:
    def __init__(self, camel_styles:dict[str, str]):
        '''Creates a pyramid of dice for the game Camel Up.'''
        self.STYLES = camel_styles
        self.DIE_VALUES = [1,2,3] #TODO
        self.DIE_COLORS = ["r", "b", "g", "y", "p"] #TODO
        self.remaining_dice = ["r", "b", "g", "y", "p"]
        self.reset_leg()
        pass 

    def shake(self):
        '''Shakes the pyramid to remove a random color from the remaining dice.

            Return
                tuple[str, int] - A tuple representation of the rolled die
                                  Ex. ("y", 2)
                                  If there are no dice remaining, return ("", 0)
        '''
        length = len(self.remaining_dice)
        if len(self.remaining_dice) == 0:
            return ("", 0)
        random_int = random.randint(0, length-1)
        color = self.remaining_dice[random_int]
        self.remaining_dice.pop(random_int)
        dice_roll = self.DIE_VALUES[random.randint(0, 2)]
        roll = (color, dice_roll)
        return roll
        pass

    def reset_leg(self):
        '''Ensures that all dice colors are returned to the pyramid
        '''
       
        self.remaining_dice = ["r", "b", "g", "y", "p"]

        pass

    def __str__(self):
        dice_str="Remaining dice: "
        for die in self.remaining_dice:
            dice_str+=self.STYLES[die[0]]+die[0]+Style.RESET_ALL+" "
        return dice_str

if __name__ == "__main__":
    STYLES= {
            "r": Back.RED+Style.BRIGHT,
            "b": Back.BLUE+Style.BRIGHT,
            "g": Back.GREEN+Style.BRIGHT,
            "y": Back.YELLOW+Style.BRIGHT,
            "p": Back.MAGENTA
    }
    pyramid = Pyramid(STYLES)
    print(pyramid)
    num_rolls=3
    for _ in range(num_rolls):
        rolled_die = pyramid.shake()
        print(f"{rolled_die} was shaken from the pyramid")
    print(pyramid)
    # testing = [["yay", "woo", "g", "h"],["doo", "goo"]] 
    # for i in range(len(testing)):
    #     if "woo" in testing[i]:
    #         outer_list = i
    #         inner_list = testing[i].index("woo")
    # stuff_to_move = testing[outer_list][inner_list:]
    # length = len(testing[outer_list][inner_list:])
    # for i in range(length):
    #     testing[outer_list].pop(inner_list)
    # #for i in range(len(stuff_to_move)):
    # testing[outer_list+1].extend(stuff_to_move)
    # print(testing)
    # dict_testing = {'r': [1], 'g': [5, 3, 3, 2]}

    # dict_testing['r'].pop(0)
    # if dict_testing['r'] == []:
    #     print(dict_testing['r'])
    # print(dict_testing)
    
    # testing_list = [[1, 2, 3, 4, 5],[],[],[]]
    # print(testing_list[0][4] +=1)
    
    # word = -1 
    # for i in testing:
    #     count = -1 
    #     word+=1
    #     for x in i:
    #         count += 1
    #         if x == 'y':
    #             print(word,count)