import random
from random import randint
from copy import deepcopy
import numpy as np


class Node:
    def __init__(self, board, parent=None):
        self.parent = parent
        self.childArray = []
        self.board = board
        self.size = len(board)
        self.numberOfVisits = 0
        self.numberOfWins = 0
        self.possibleActions = None

    def select(self, c, t):
        listUCB = []
        for child in self.childArray:
            if child.numberOfVisits == 0:
                listUCB.append(1000000) #on met un très grand nombre pour être sûr que cet enfant soit visité au moins une fois
            else:
                listUCB.append((child.numberOfWins / child.numberOfVisits) + c * np.sqrt(np.log(t) / child.numberOfVisits))
        return self.childArray[np.argmax(listUCB)]

    def expand(self):
        action = self.possibleActions.pop()
        childNode = Node(deepcopy(self.board), parent=self) #si on met direct self.board, l'enfant et le parent auront tous les 2 la même array avec 2 références différentes. La modification dans un des objets impactera l'array et cette modification sera visible dans l'autre objet
        childNode.board[action] = 1
        self.childArray.append(childNode)
        return childNode #comment le return sait que childNode est dans self ? Il ne retourne pas juste un objet ?

    def simulate(self):
        simulation = deepcopy(self.board)
        toFill = [i for i, item in enumerate(self.board) if item == 0]
        while toFill:
            simulation[toFill.pop()] = randint(1, 2)
        c1 = simulation.count(1)
        c2 = simulation.count(2)
        if c1 > c2:
            return 1
        else:
            return 2

    def backPropagate(self, winner):
        self.numberOfVisits += 1
        if winner == 1:
            self.numberOfWins += 1
        if self.parent:
            self.parent.backPropagate(winner)

    def updatePossibleActions(self):
        emptySlots = []
        for i in range(self.size):
            if len(emptySlots) > 1:
                break
            if self.board[i] == 0:
                emptySlots.append(i)
        random.shuffle(emptySlots)
        self.possibleActions = emptySlots


def alternate():
    while True:
        yield 1
        yield 2


if __name__ == '__main__':
    board = [0] * 3
    root = Node(board)

    time = 400
    t = 0
    for i in range(time):
        t += 1
        node = root
        while node.childArray:
            node = node.select(np.sqrt(2), t)
        print("selected " + str(node.board))
        node.updatePossibleActions()
        while node.possibleActions:
            node.expand()
        for x in node.childArray:
            print(x.board)
        a = randint(0, len(node.childArray)-1)
        print("choix : " + str(a))
        child = node.childArray[a]
        w = child.simulate()
        #print("winner : " + str(w))
        child.backPropagate(w)
        print("temps : " + str(t))


"""
alternator = alternate()
    player = alternator.__next__()
"""