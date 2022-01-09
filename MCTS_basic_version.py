import random
from random import randint
from copy import deepcopy
import numpy as np


class Node:
    def __init__(self, board, player=None, parent=None):
        self.board = board
        self.size = len(board)
        self.player = player
        self.parent = parent
        self.childArray = []
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
        childNode = Node(deepcopy(self.board), player=3-self.player, parent=self) #si on met direct self.board, l'enfant et le parent auront tous les 2 la même array avec 2 références différentes. La modification dans un des objets impactera l'array et cette modification sera visible dans l'autre objet
        childNode.board[action] = self.player
        self.childArray.append(childNode)
        return childNode

    def simulate(self):
        tempoNode = Node(deepcopy(self.board), player=3-self.player)
        while checkStatus(tempoNode.board) == -1:
            tempoNode.randomMove()
        return checkStatus(tempoNode.board)

    def backPropagate(self, winner):
        self.numberOfVisits += 1
        if winner == self.player:
            self.numberOfWins += 1
        if self.parent:
            self.parent.backPropagate(winner)

    def updatePossibleActions(self):
        emptySlots = []
        colonnes = [0] * 7
        for i in range(self.size):
            if self.board[i] == 0:
                emptySlots.append(i)
        random.shuffle(emptySlots)
        self.possibleActions = emptySlots

    def randomMove(self):
        self.updatePossibleActions()
        self.board[self.possibleActions.pop()] = self.player
        self.player = 3-self.player


def checkStatus(board):
    l = len(board)
    if board[l - 2] == board[l - 1] != 0:  # le joueur qui met ses pionts sur les 2 dernières cases gagne
        return board[l - 2]
    elif 0 in board: #la partie n'est pas finie
        return -1
    else: #égalité
        return 0


def bestMove(board, player):
    c = np.sqrt(2)
    root = Node(board, player=player)
    time = 400

    for t in range(time):
        node = root
        while node.childArray:
            node = node.select(c, t)
        node.updatePossibleActions()
        if node.possibleActions:
            while node.possibleActions:
                node.expand()
            a = randint(0, len(node.childArray) - 1)
            child = node.childArray[a]
            w = child.simulate()
        else:  # la simulation est arrivée à un noeud final qui ne peut pas être expand ni simulé car il correspond à un état final du jeu
            child = node
            w = checkStatus(child.board)
        child.backPropagate(w)

    return root.select(c, time).board


if __name__ == '__main__':
    board = [0] * 9
    currentPlayer = 2

    for i in range(9):
        board = bestMove(board, currentPlayer)
        currentPlayer = 3 - currentPlayer
        #print("player : " + str(currentPlayer))
        if checkStatus(board) != -1:
            break

    print(board)
    print("winner is : " + str(checkStatus(board)))
