#####################

# Hi there! To run this game, just download python 3 and double click this file.
# The visual effects with os.system('cls') only look pretty on the console.
# However it can also be played on shell but will look ugly af.
# Enjoy !!! 

#####################

# Imports

from time import sleep # pause for a few seconds - mimics realistic thinking/loading effects
from random import shuffle # easy way to shuffle the deck
import os; clear = lambda: os.system('cls') # for realistic board effects when run in console
import pdb; trace = lambda: pdb.set_trace() # for debugging

# Notes
# [D] (Display) indicates a list of actual cards (K, J, 2, 3, A, etc.) ! is small joker, !! is big joker
# [C] (Code) indicates a list of card power values (3 -> power 3, 10 -> power 10, K -> power 13, !! -> power 17, etc.)

# Classes

class Cards: # Takes a hand in [D] or [C] form, and returns a properly sorted [D] or [C] form
    def __init__(self, hand, hand_type):
        self.display = []
        self.code = []
        display_values = ['3','4','5','6','7','8','9','10','J','Q','K','A','2','!','!!']
        code_values =    [3,   4,  5,  6,  7,  8,  9,  10,  11, 12, 13, 14, 15, 17, 18]
        # code_value jumps from 15 to 17 for ease of straight parsing in opps_turn()
        

        if hand_type == '[D]':
            # Make [C] 
            for i in hand: # add the relevant power values
                if i == 'T': # add [10]
                    self.code.append(10)
                elif i not in ['T','!']: # add the card as is
                    self.code.append(code_values[display_values.index(i)])
            if hand.count('!') == 1: # add small joker
                self.code.append(17)
            elif hand.count('!') == 2: # add big joker
                self.code.append(18)
            elif hand.count('!') == 3: # add both jokers
                self.code.append(17)
                self.code.append(18)
            self.code.sort()

            # Make [D]
            for i in self.code:
                self.display.append(display_values[code_values.index(i)])

        elif hand_type == '[C]':
            hand.sort()

            #Make [C]
            self.code = list(hand)

            # Make [D]
            for i in self.code:
                self.display.append(display_values[code_values.index(i)])

# Methods

def your_turn(table):
    show(table)

    hand = []
    combo = ''
    power = 0

    # take input for the hand you want to play. replace '10' with 't' for parsing ease
    hand = list(str.upper(input('Go: ').replace('10','t')))

    # go to opponent's turn when you pass
    if hand == ['P','A','S','S'] or hand == ['P']: 
        table['cards'].append('pass')

        show(table)
        
        table['cards'] = []
        table['combo'] = ''
        table['power'] = 0

        sleep(1)
        opps_turn(table)
        
    # get new input if some invalid character entered
    for i in hand:
        if i not in '3456789TJQKA2!':
            your_turn(table)

    # if no pass
    # define local variables for what you played in [D] and [C] format
    display = Cards(hand, '[D]').display
    code = Cards(hand, '[D]').code

    # does you actually have the cards to play? yes = do nothing, no = get new input
    if any([code.count(i) > table['your_hand'].count(i) for i in code]) or code == []:
        your_turn(table)

    # can the user actually play the combo legally in the game?
    
    # 'validate method' (see if what you played beats the current board)
    # check win
    # opponent turn (must find a less absurd way of doing the AI)
    
    # what is the combo user played? and the power? assigns to variables
    # functionality of below relies on hands being properly sorted
    if len(code) == 1:        
        combo = 'single'
        power = sum(code)
    elif len(code) == 5 and \
         code[0]==code[1]-1==code[2]-2==code[3]-3==code[4]-4 and \
         code[4] <= 14: # string can only range from [3] to [A]
        combo = 'straight'
        power = sum(code)
    elif len(code) == 5 and ( \
         code[0]==code[1] and code[2]==code[3]==code[4] or
         code[0]==code[1]==code[2] and code[3]==code[4]):
        combo = 'full'
        power = sum(code[2:5]) if code[2]==code[3]==code[4] else sum(code[0:3])
    elif len(code) == 5 and (\
         code[0]==code[1]==code[2]==code[3] or \
         code[1]==code[2]==code[3]==code[4]) or \
         len(code) == 4 and \
         code[0]==code[1]==code[2]==code[3]:
        combo = 'bomb'
        if code[0]==code[1]==code[2]==code[3]:
            power = sum(code[1:5])+10000 # bomb beats everything except a bigger bomb
        elif code[1]==code[2]==code[3]==code[4]:
            power = sum(code[0:4])+10000 # bomb beats everything except a bigger bomb
        # note there is no need to include the power value of the single attachment
    elif len(code) % 2 == 0 and \
         all([code[i]==code[i+1] for i in range(0, len(code)-2, 2)]) and \
         all([code[i]==code[i+2]-1 for i in range(0, len(code)-2, 2)]):
        combo = 'chainpair' + str(len(code)//2)
        power = sum(code)
    elif len(code) % 3 == 0 and \
         all([code[i]==code[i+1]==code[i+2] for i in range(0, len(code)-3, 3)]) and \
         all([code[i]==code[i+3]-1 for i in range(0, len(code)-3, 3)]):
        combo = 'chaintriplet' + str(len(code)//3)
        power = sum(code)

    # if users hand beats the board, proceed with game flow
    if hand_beats_board_bool(code, combo, power, table):
        for i in code:
            table['your_hand'].remove(i)
        table['cards'].append(''.join(Cards(code, '[C]').display) + ' ->')
        table['combo'] = combo
        table['power'] = power

        show(table)

        # did you win?
        if len(table['your_hand']) == 0:
            show(table)
            sleep(1)
            process_win('You')

        sleep(1)    
        opps_turn(table)
    
    your_turn(table)

def opps_turn(table):
    # 1. creates a list of all [C] combos the opponent could play, from weakest to strongest
    # 2. tests validity of all combos, and plays the weakest valid one
    # 3. if none valid, pass
    show(table)

    hand = [] # all possible hands opponent can play (lists)
    combo = [] # all combo types of above (strings)
    power = [] # all power values of above (integers)

    test_hand = [] # current hand to be iterated and tested for validity

    # STRAIGHTS
    if table['combo'] == 'straight' or table['combo'] == '':
        relevant_hand = [i for i in table['opps_hand'] if table['opps_hand'].count(i) != 4]
        # add straights
        for i in relevant_hand:
            test_hand = [i,i+1,i+2,i+3,i+4]
            if set(test_hand).issubset(set(relevant_hand)):
                if list(map(lambda x: relevant_hand.count(x) == 1, test_hand)).count(True) >= 3 and \
                   test_hand not in hand:
                    # 'ai': only considers straights that are 'efficient' and contain 3 or more singles
                    hand.append(test_hand)
                    combo.append('straight')
                    power.append(sum(test_hand))
                
        # add fulls; full beat straight
        for i in relevant_hand:
            if relevant_hand.count(i) == 3:
                for j in relevant_hand:
                    test_hand = [j,j,i,i,i]
                    if relevant_hand.count(j) >= 2 and j != i and test_hand not in hand:
                        # 'ai': will pull [x,x] from [x,x,x]
                        hand.append(test_hand)
                        combo.append('full')
                        power.append(i*3)
                        break

    # CHAINPAIRS
    if 'chainpair' in table['combo'] or table['combo'] == '':
        relevant_hand = list(set([i for i in table['opps_hand'] if table['opps_hand'].count(i) not in [1,4]]))
        # list of all cards in opps_hand with count of 2 or 3, without duplicates
        # duplicates are removed for simpler parsing below, as singles are filtered out already
        chain_length = [i for i in range(1, 10)] if table['combo'] == '' else [int(table['combo'][-1])]
        chain_length.reverse()
        
        # add chainpairs
        for h in chain_length:
            for i in relevant_hand:
                test_hand = [i + j for j in range(h)]
                if set(test_hand).issubset(set(relevant_hand)):
                    if list(map(lambda x: table['opps_hand'].count(x) == 3, test_hand)).count(True) <= h / 2:
                        # 'ai': only considers chainpairs that don't break up more triplets than pairs / 2 
                        if test_hand not in hand:
                            hand.append(sorted(test_hand * 2))
                            combo.append('chainpair' + str(h))
                            power.append(sum(sorted(test_hand * 2)))

    # CHAINTRIPLETS
    if 'chaintriplet' in table['combo'] or table['combo'] == '':
        relevant_hand = list(set([i for i in table['opps_hand'] if table['opps_hand'].count(i) == 3]))
        # list of all cards in opps_hand with count of 2 or 3, without duplicates
        # duplicates are removed for simpler parsing below, as singles are filtered out already
        chain_length = [i for i in range(1, 7)] if table['combo'] == '' else [int(table['combo'][-1])][::-1]
        chain_length.reverse()
        
        # add chaintriplets
        for h in chain_length:
            for i in relevant_hand:
                test_hand = [i + j for j in range(h)]
                if set(test_hand).issubset(set(relevant_hand)): 
                    if test_hand not in hand:
                        hand.append(sorted(test_hand * 3))
                        combo.append('chaintriplet' + str(h))
                        power.append(sum(sorted(test_hand * 3)))
                        
    # FULLS
    if table['combo'] == 'full' or table['combo'] == '':
        relevant_hand = [i for i in table['opps_hand'] if table['opps_hand'].count(i) not in [1,4]]

        # add fulls
        for i in relevant_hand:
            if relevant_hand.count(i) == 3:
                for j in relevant_hand:
                    test_hand = [j,j,i,i,i]
                    if relevant_hand.count(j) >= 2 and j != i and test_hand not in hand:
                        # 'ai': will pull [x,x] from [x,x,x]
                        hand.append(test_hand)
                        combo.append('full')
                        power.append(i*3)
                        break
                             
    # SINGLES
    if table['combo'] == 'single' or table['combo'] == '':
        relevant_hand = list(set([i for i in table['opps_hand']]))
        singles_to_be_added = []
        # add singles not in straights
        # add singles in triplets
        # add singles in straights
        # add singles in pairs
        # add singles in bombs

        singles_to_be_added += [i for i in relevant_hand if table['opps_hand'].count(i) == 1 and \
                                not set([i,i+1,i+2,i+3,i+4]).issubset(set(table['opps_hand']))]
        singles_to_be_added += [i for i in relevant_hand if table['opps_hand'].count(i) == 3]
        singles_to_be_added += [i for i in relevant_hand if table['opps_hand'].count(i) == 1 and \
                                set([i,i+1,i+2,i+3,i+4]).issubset(set(table['opps_hand']))]
        singles_to_be_added += [i for i in relevant_hand if table['opps_hand'].count(i) == 2]
        singles_to_be_added += [i for i in relevant_hand if table['opps_hand'].count(i) == 4]      

        for i in singles_to_be_added:
            hand.append([i])
            combo.append('single')
            power.append(i)

    # BOMBS (does not include single attachment yet
    if True:
        relevant_hand = [i for i in table['opps_hand'] if table['opps_hand'].count(i) == 4]
        
        for i in relevant_hand:
            test_hand = [i,i,i,i]
            if test_hand not in hand:
                hand.append(test_hand)
                combo.append('bomb')
                power.append(sum(test_hand)+10000)

    # ply some hand, or pass
    hand.append('pass')
    for i in range(len(hand)):
        if hand[i] == 'pass':
            table['cards'].append('pass')
            show(table)

            table['cards'] = []
            table['combo'] = ''
            table['power'] = 0

            sleep(1)
            your_turn(table)

        if hand_beats_board_bool(hand[i], combo[i], power[i], table):
            for j in hand[i]:
                table['opps_hand'].remove(j)
            table['cards'].append(''.join(Cards(hand[i], '[C]').display) + ' ->')
            table['combo'] = combo[i]
            table['power'] = power[i]
            
            break

    # did opponent win?
    if len(table['opps_hand']) == 0:
        show(table)
        sleep(1)
        process_win('Opponent')

    sleep(1)
    your_turn(table)

def process_win(player): # once a player wins, this stuff happens
    print(player + ' win :)')
    while True:
        x = str.upper(input('\'n\': New Game, \'x\': Exit: '))
        if x == 'N':
            clear()
            main()
        elif x == 'X':
            exit()
                 
def hand_beats_board_bool(code, combo, power, table):
    # does the hand 'code' with 'combo' and 'power' beat what is currently on the table?
    # if yes, return True, if no, return False

    # the four success conditions (full>straight, bomb>notbomb, stronger>weaker, all>empty board)
    if combo == 'full' and table['combo'] == 'straight' or \
        combo == 'bomb' and table['combo'] != 'bomb' or \
        combo == table['combo'] and power > table['power'] or \
        combo != '' and table['combo'] == '' and table['power'] == 0:
        return True
    else:
        return False

def new_game(): # declares fresh variables for a new game, and starts your turn
    deck = [3]*4 + [4]*4 + [5]*4 + [6]*4 + [7]*4 + [8]*4 + [9]*4 + \
           [10]*4 + [11]*4 + [12]*4 + [13]*4 + [14]*4 + [15]*4 + [17, 18]
    shuffle(deck)

    table = {'your_hand':sorted(list(deck[:18])), 'opps_hand':sorted(list(deck[-18:])), \
             'cards':[], 'combo':'', 'power':0}

    your_turn(table)
    
def show(table): # shows/refreshes the table
    clear()
    print('\nOpponent:\n[{}]'.format('] ['.join(['#']*len(table['opps_hand']))))
    # Enable above line to conceal opponent's hand (realistic)
    # Enable below line to reveal opponent's hand (cheating)
    #print('\nOpponent:\n[{}]'.format('] ['.join(Cards(table['opps_hand'], '[C]').display)))
    
    print('\nTable: {}'.format(' '.join(table['cards'])))
    print('\nYou:\n[{}]'.format('] ['.join(Cards(table['your_hand'], '[C]').display)))

def main(): # main function containing instructions
    print('Welcome to Zheng Shang You! ')

    while True:
        x = str.upper(input('\'h\'      : how to play\n\'any key\': play: '))
        if x == 'H':
            clear()
            print('\n\
                Single            [3]                   \n\
                Pair              [4][4]                \n\
                Triplet           [5][5][5]             \n\
                Straight          [3][4][5][6][7]       Can\'t include [2] or [!]! Must be length 5!\n\
                Full House        [8][8][8][9][9]       Kills all Straight!\n\
                Chain Pair     [10][10][J][J][Q][Q]  Can be any length!\n\
                Chain Triplet  [K][K][K][A][A][A]    Can be any length!\n\
                Bomb              [2][2][2][2]([3])     Kills everything! Optional: carry extra card!\n\
                \n\
                \'pass\' or \'p\': pass\n\
                [!]          : little joker\n\
                [!!]         : big joker')
            input()
            new_game()
        else:
            new_game()

       
main()
