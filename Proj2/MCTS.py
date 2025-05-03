import math
import random
import time
from handRank import ranker

# value present in slides on MCTS
C = math.sqrt(2)

# simple node with relevant table info and backpropagation for tree
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.terminal = False

    def add_child(self, child_state):
        child = Node(child_state, parent=self)
        self.children.append(child)
        return child
    
# UCB1 for balancing exploration and exploitation
def UCB1(node):
    (node.wins / node.visits) + C * math.sqrt(math.log(node.parent.visits) / node.visits)

# tree search
# start at our cards plus the current round's community cards
def MCTS(root, deck, hand, table, round, limit = 10):
    i = 0
    start = time.perf_counter()
    while ((time.perf_counter() - start) <= limit):
        i += 1
        print(f"\rSimulation Count: {i}", end='', flush=True)
        node = root
        deck_cpy = deck.copy()
        table_cpy = table.copy()
        # selection - find non terminal leaf with highest UCB1
        while not node.terminal and len(node.children) != 0:
            UCB1s = [(child, UCB1(child)) for child in node.children]
            node = max(UCB1s, key=lambda x: x[1])[0]

        # expansion - expand from leaf with new states
#       ∗ Simulate random possible opponent hole cards
#       ∗ Simulate random future community cards

        # pull opp cards
        random.shuffle(deck_cpy)
        opp = deck_cpy[-2:]
        del (deck_cpy[-2:])

        # pull remaining cards depending on round coming into tree
        if round == 0:
            table_cpy.extend(deck_cpy[-5:])
        elif round == 1:
            table_cpy.extend(deck_cpy[-2:])
        else:
            table_cpy.extend(deck_cpy[-1:])

        node = node.add_child(table_cpy)

        # simulation
        # rank hand against opp

        oppScore = ranker(opp + table_cpy)
        botScore = ranker(hand + table_cpy)
        win = 0
        if botScore > oppScore:
            win = 1

        node.terminal = True

        # backpropagation
        while node is not None:
            node.wins += win
            node.visits += 1
            node = node.parent

    return root.wins/root.visits

