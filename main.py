import random
from random import randint
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
            if len(emptySlots) > 4:
                break
            if self.board[i] is None:
                emptySlots.append(i)
        random.shuffle(emptySlots)
        print(emptySlots)
        self.possibleActions = emptySlots

    def checkStatus(self):
        if self.board[0] == 0:
            return 0
        elif self.board[0] == 1:
            return 1
        else:
            return -1

    def select(self):
        listUCB = [x.numberOfWins for x in self.childArray]
        return self.childArray[np.argmax(listUCB)]

    def expand(self):
        action = self.possibleActions.pop()
        print(action)
        #print(self.board)
        childNode = Node(self.board, parent=self)
        #print(self.board)
        childNode.board[action] = 1
        #print(childNode, childNode.parent, self)
        #print(childNode.board, childNode.parent.board, self.board)
        self.childArray.append(childNode)
        return childNode #comment le return sait que childNode est dans self ? Il ne retourne pas juste un objet ?

    def simulate(self):
        self.board[randint(0, 8)] = 9

    def backPropagate(self):
        self.numberOfVisits += 1
        print(self.numberOfVisits)
        if self.parent:
            self.parent.backPropagate()


def alternate():
    while True:
        yield 1
        yield 2


if __name__ == '__main__':
    board = [0] * 9
    root = Node(board)

    t = 2
    for i in range(t):
        node = root
        while node.childArray:
            print("on descend")
            node = node.select()
        print("selected " + str(node.board))
        node.updatePossibleActions()
        while node.possibleActions:
            node.expand()
            for x in node.childArray:
                print(x.board)
        #print(len(node.childArray))
        a = randint(0, len(node.childArray)-1)
        print(a)
        child = node.childArray[a]
        child.simulate()

        child.backPropagate()



"""
alternator = alternate()
    player = alternator.__next__()
    
    jeu = Board(4)
    jeu.updateBoard(1,0)
    node1 = Node(1)
    nodea = node1
    for i in range(5):
        nodeb = nodea.expand()
        nodea = nodeb

    print(node1.move)
    print(node1.childArray[0].move)
    print(node1.childArray[0].childArray[0].move)
    print(node1.childArray[0].childArray[0].childArray[0].move)
    print(node1.childArray[0].childArray[0].childArray[0].childArray[0].move)
    print(node1.childArray[0].childArray[0].childArray[0].childArray[0].childArray[0].move)
"""