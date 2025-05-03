import random
from MCTS import MCTS, Node
from handRank import ranker

# cards are 0-51
# suit is card // 13
# rank is card % 13 
    
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
tree_deck = deck # save the opp cards because bot doesn't know what they are
opp = deck[-4:-2]

del deck[-4:]

print(bot)
print(opp)

# run mcts, decide if win is >50

root = Node([], None)
fold = MCTS(root, tree_deck, bot, table=[], round=1, limit=10)
if fold < 0.5:
    print("Fold!")
    exit

# actual flop
flop = flop(deck)
print(flop)
tree_deck = deck

# run mcts, decide if win is >50

fold = MCTS(root, tree_deck, bot, table=flop, round=2, limit=10)
if fold < 0.5:
    print("Fold!")
    exit

# actual turn
turn = turn(deck, flop)
print(turn)
tree_deck = deck

# run mcts, decide if win is >50

fold = MCTS(root, tree_deck, bot, table=turn, round=3, limit=10)
if fold < 0.5:
    print("Fold!")
    exit

# actual river
river = river(deck, turn)
print(river)

# determine winner, or we folded
opp_actual = ranker(opp + river)
bot_actual = ranker(bot + river)

if bot_actual > opp_actual:
    print("Win!")
elif bot_actual < opp_actual:
    print("Loss")
else:
    print("Tie")
