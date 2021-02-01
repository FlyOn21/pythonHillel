import random
import sys
import math

# 1) Write a function that emulates the game "rock, scissors, paper"
# At the entrance, your function accepts your version printed from the console, the computer makes a decision randomly.
class Game_Rock_Scissors_Paper():
    """Class implemented logic game 'rock, scissors, paper'"""
    def __init__(self):
        self.tuple_combination_win = (('rock', 'scissors'), ('scissors', 'paper'), ('paper', 'rock'))
        self.tuple_combination_draw = (('rock', 'rock'), ('scissors', 'scissors'), ('paper', 'paper'))
        self.dict_variations_input = {'1': 'rock', '2': 'scissors', '3': 'paper'}
        self.mistake_counter = 0
        self.replay_counter = 0

    def main(self):
        people_choice = self.my_choice()
        if people_choice is not False:
            comp_choice = self.cumputer_choice()
            result = self.who_winnings(my_choice_input=people_choice, cumputer_choice_input=comp_choice)
            print(result)
            self.play_agaen()
        else:
            print('May be you don\'t want play. By-by')
            sys.exit()


    def my_choice(self):
        if self.check_counter() is not False:
            my_choice_input = str(input('Please input your choice (1 - rock, 2 - scissors, 3 - paper) : '))
            if my_choice_input not in self.dict_variations_input.keys():
                self.mistake_counter += 1
                print('You entered incorrect data, please re-enter. Choose between 1 - rock, 2 - scissors, 3 - paper')
                return self.my_choice()
            else:
                self.mistake_counter = 0
                return self.dict_variations_input[my_choice_input]
        else:
            return False

    def check_counter(self):
        if self.mistake_counter == 5:
            return False
        else:
            return True

    def cumputer_choice(self):
        values = [values for values in self.dict_variations_input.values()]
        comp_choice_input = random.choice(values)
        return comp_choice_input

    def who_winnings(self, my_choice_input, cumputer_choice_input):
        all_choice = (my_choice_input, cumputer_choice_input)
        if all_choice in self.tuple_combination_win:
            return f'You win! {my_choice_input} wins {cumputer_choice_input}'
        elif all_choice in self.tuple_combination_draw:
            return f'Draw,you both choice {cumputer_choice_input}'
        else:
            return f'You lose! {cumputer_choice_input} wins {my_choice_input}'

    def play_agaen(self):
        repeat = str(input('You want play agen. Please entered "n" - NO or "y" - YES: ')).lower()
        if repeat == 'n':
            print('By - by')
            sys.exit()
        elif repeat == 'y':
            self.replay_counter = 0
            self.main()
        else:
            print('I did not understand you.')
            self.replay_counter +=1
            if self.replay_counter == 5:
                print('By -by')
            else:
                return self.play_agaen()

# 2)Try to imagine a world in which you might have to stay home for (Corona virus) 14 days at any given time.
# Do you have enough toilet paper(TP) to make it through?
# Although the number of squares per roll of TP varies significantly, we'll assume each roll has 500 sheets,
# and the average person uses 57 sheets per day.
# Create a function that will receive a dictionary with two key/values:
# "people" ⁠— Number of people in the household.
# "tp" ⁠— Number of rolls.
# Return a statement telling the user if they need to buy more TP!
def toilet_paper_supply(dict_tp=None):
    """Function determines if there is enough toilet paper for a family for 14 days"""
    if dict_tp is None:
        dict_tp = {'people': 3, 'tp': 8}
    stock_for_14_days = dict_tp['people']* 57 * 14
    toilet_paper_now = dict_tp['tp'] * 500
    if stock_for_14_days < toilet_paper_now:
        return 'Enough toilet paper for a family for 14 days'
    else:
        lock_of_total_paper_rolls = math.ceil((stock_for_14_days - toilet_paper_now) / 500)
        return f'Need to buy {lock_of_total_paper_rolls} rolls'

# 3) Make a function that encrypts a given input with these steps:
# Input: "apple"
# Step 1: Reverse the input: "elppa"
# Step 2: Replace all vowels using the following chart:
# a => 0
# e => 1
# i => 2
# o => 2
# u => 3
# # "1lpp0"
# Example:
# encrypt("banana") ➞ "0n0n0baca"
# encrypt("karaca") ➞ "0c0r0kaca"
# encrypt("burak") ➞ "k0r3baca"
# encrypt("alpaca") ➞ "0c0pl0aca"
def encrypt_data(given_input='banana', encrypt_dict=None):
    """Function implemented processing encrypt given input"""
    if encrypt_dict is None:
        encrypt_dict = {'a': '0', 'e': '1', 'i': '2', 'o': '2', 'u': '3'}
    first_step = [char for char in reversed(given_input)]
    second_step = []
    for char in first_step:
        if char in encrypt_dict.keys():
            char = encrypt_dict[char]
            second_step.append(char)
        else:
            second_step.append(char)
    result = ''.join(second_step)
    return result

# **4)Given a 3x3 matrix of a completed tic-tac-toe game, create a function that returns whether the game is a win
# for "X", "O", or a "Draw", where "X" and "O" represent themselves on the matrix, and "E" represents an empty spot.
# Example:
# tic_tac_toe([
#     ["X", "O", "X"],
#     ["O", "X", "O"],
#     ["O", "X", "X"]
# ]) ➞ "X"
#
# tic_tac_toe([
#     ["O", "O", "O"],
#     ["O", "X", "X"],
#     ["E", "X", "X"]
# ]) ➞ "O"
#
# tic_tac_toe([
#     ["X", "X", "O"],
#     ["O", "O", "X"],
#     ["X", "X", "O"]
# ]) ➞ "Draw"

def main(tic_tac_toe):
    """Function defines who winning in 3x3 matrix of a completed tic-tac-toe game"""
    game_board = join_array(tic_tac_toe)
    marks = ['X', 'O']
    for mark in marks:
        if win_check(game_board, mark) is True:
            return f'Win "{mark}"'
    else:
        return 'Draw'


def join_array(tic_tac_toe):
    """Function unpacking 3x3 matrix in list"""
    general_array = [*tic_tac_toe[0], *tic_tac_toe[1], *tic_tac_toe[2]]
    return general_array


def win_check(game_board, mark):
    """Function check winnig combination in game"""
    if mark == game_board[0] and mark == game_board[1] and mark == game_board[2]:
        return True
    elif mark == game_board[3] and mark == game_board[4] and mark == game_board[5]:
        return True
    elif mark == game_board[6] and mark == game_board[7] and mark == game_board[8]:
        return True
    elif mark == game_board[0] and mark == game_board[4] and mark == game_board[8]:
        return True
    elif mark == game_board[2] and mark == game_board[4] and mark == game_board[6]:
        return True
    elif mark == game_board[0] and mark == game_board[3] and mark == game_board[6]:
        return True
    elif mark == game_board[2] and mark == game_board[5] and mark == game_board[8]:
        return True
    elif mark == game_board[1] and mark == game_board[4] and mark == game_board[7]:
        return True
    return False


if __name__ == '__main__':
    print('Task #1')
    game = Game_Rock_Scissors_Paper()
    game.main()

    # print('Task #2')
    # result = toilet_paper_supply()
    # print(result)
    #
    # print('Task #3')
    # result = encrypt_data()
    # print(result)
    #
    # print('Task #4')
    # result = main(tic_tac_toe)
    # print(result)
