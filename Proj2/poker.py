import random
from MCTS import MCTS, Node
from handRank import ranker

# cards are 0-51
# suit is card // 13
# rank is card % 13 
    
# makes the int cards readable
def toCard(card):
    suit = card // 13
    rank = card % 13
        
    ranks = "23456789TJQKA"
    suits = "CDHS"
    rank_str = ranks[rank]
    suit_str = suits[suit]
    return rank_str + suit_str

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

print([toCard(card) for card in bot])
print([toCard(card) for card in opp])

# run mcts, decide if win is >=50

root = Node([], None)
fold = MCTS(root, tree_deck, bot, table=[], round=0, limit=10)
print("\nPreflop win %: ")
print(fold)
if fold < 0.5:
    print("Fold!")
    exit()
else:
    print("Stay!")

# actual flop
flop = flop(deck)
print([toCard(card) for card in flop])
tree_deck = deck

# run mcts, decide if win is >=50

fold = MCTS(root, tree_deck, bot, table=flop, round=1, limit=10)
print("\nPreturn win %: ")
print(fold)
if fold < 0.5:
    print("Fold!")
    exit()
else:
    print("Stay!")

# actual turn
turn = turn(deck, flop)
print([toCard(card) for card in turn])
tree_deck = deck

# run mcts, decide if win is >=50

fold = MCTS(root, tree_deck, bot, table=turn, round=2, limit=10)
print("\nPre-River win %: ")
print(fold)
if fold < 0.5:
    print("Fold!")
    exit()
else:
    print("Stay!")

# actual river
river = river(deck, turn)
print([toCard(card) for card in river])

# determine winner, or we folded earlier
opp_actual = ranker(opp + river)
bot_actual = ranker(bot + river)

if bot_actual > opp_actual:
    print("Win!")
elif bot_actual < opp_actual:
    print("Loss")
else:
    print("Tie")
