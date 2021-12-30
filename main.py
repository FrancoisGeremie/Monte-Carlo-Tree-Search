from random import randint
import numpy as np

class Board:
    def __init__(self, size):
        self.size = size
        self.board = [None]*size

    def updateBoard(self, player, position):
        self.board[position] = player

    def checkStatus(self):
        if self.board[0] == 0:
            return 0
        elif self.board[0] == 1:
            return 1
        else:
            return -1

    def randomMove(self):
        value = randint(0, 9)
        self.board.updateBoard(1, value)


class Node:
    def __init__(self, move, parent=None):
        self.move = move
        self.parent = parent
        self.childArray = []
        self.board = Board(9)
        self.numberOfVisits = None
        self.numberOfWins = None
        self.UCB = None

    def expand(self):
        move = randint(0, 9)
        childNode = Node(move, parent=self)
        self.childArray.append(childNode)
        return childNode #comment le return sait que childNode est dans self ? Il ne retourne pas juste un objet ?

    def select(self):
        listUCB = [self.UCB for x in self.childArray]
        return self.childArray[np.argmax(listUCB)]

    def backPropagate(self):
        self.move +=1
        #print(self.move)
        if self.parent:
            self.parent.backPropagate()


if __name__ == '__main__':
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

    nodeb.backPropagate()

    print(node1.move)
    print(node1.childArray[0].move)
    print(node1.childArray[0].childArray[0].move)
    print(node1.childArray[0].childArray[0].childArray[0].move)
    print(node1.childArray[0].childArray[0].childArray[0].childArray[0].move)
    print(node1.childArray[0].childArray[0].childArray[0].childArray[0].childArray[0].move)