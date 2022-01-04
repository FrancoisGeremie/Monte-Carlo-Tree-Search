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

    def updatePossibleActions(self):
        emptySlots = []
        for i in range(self.size):
            if len(emptySlots) > 3:
                break
            if self.board[i] == 0:
                emptySlots.append(i)
        random.shuffle(emptySlots)
        print(emptySlots)
        self.possibleActions = emptySlots

    def select(self, c, t):
        listUCB = [((x.numberOfWins/x.numberOfVisits)+c*np.sqrt(np.log(t)/x.numberOfVisits)) for x in self.childArray]
        print(listUCB)
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
            simulation[toFill.pop()] = randint(3,4)
        return determineWinner(simulation)

    def backPropagate(self, winner):
        self.numberOfVisits += 1
        if winner == 1:
            self.numberOfWins += 1
        print(self.numberOfVisits)
        if self.parent:
            self.parent.backPropagate(winner)


def determineWinner(simulation):
    c1 = simulation.count(3)
    c2 = simulation.count(4)
    if c1 > c2:
        return 1
    else:
        return 2


def alternate():
    while True:
        yield 1
        yield 2


if __name__ == '__main__':
    board = [0] * 9
    root = Node(board)

    time = 2
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
        a = randint(0, len(node.childArray)-1)
        print(a)
        child = node.childArray[a]
        w = child.simulate()
        for x in node.childArray:
            print(x.board)
        print("winner : " + str(w))
        child.backPropagate(w)



"""
alternator = alternate()
    player = alternator.__next__()

"""