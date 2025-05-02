import random

# cards are 0-51
# suit is card // 13
# rank is card % 13 

# store deck as list, copy each simulation to make mutable and remove cards

# TODO: monte carlo search tree

# each node holds independent wins and visits, so the sum at the root is win/simulation = win% for decision
    
def flop(deck):
    flop = deck[-3:]
    del deck[-3:]
    return flop

def turn(deck, flop):
    flop.append(deck[44])
    del deck[-1:]
    return flop

def river(deck, turn):
    turn.append(deck[43])
    del deck[-1:]
    return turn

deck = [x for x in range(52)]
random.shuffle(deck)

# deal (actual opp cards)
bot = deck[-2:]
opp = deck[-4:-2]
del deck[-4:]

print(bot)
print(opp)

# run mcts, decide if win is >50

# actual flop
flop = flop(deck)
print(flop)

# run mcts, decide if win is >50

# actual turn
turn = turn(deck, flop)
print(turn)

# run mcts, decide if win is >50

# actual river
river = river(deck, turn)
print(river)

# determine winner, or we folded