import random
from random import randint
from copy import deepcopy
import numpy as np


class Node:
    def __init__(self, board, player=None, parent=None, move=None):
        self.board = board
        self.size = len(board)
        self.player = player
        self.parent = parent
        self.childArray = []
        self.numberOfVisits = 0
        self.numberOfWins = 0
        self.possibleActions = None
        self.move = move

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
        childNode = Node(deepcopy(self.board), player=3-self.player, parent=self, move=action) #si on met simplement self.board, l'enfant et le parent auront tous les 2 la même array avec 2 références différentes. La modification dans un des objets impactera l'array et cette modification sera visible dans l'autre objet
        childNode.board[action] = self.player
        self.childArray.append(childNode)
        return childNode

    def simulate(self):
        if 0 not in self.board: #child ne contient plus de case vide => son parent n'en avait plus qu'une
            return self.checkStatus()
        tempoNode = Node(deepcopy(self.board), player=3-self.player, move=self.move)
        while tempoNode.checkStatus() == -1:
            tempoNode.randomMove()
        return tempoNode.checkStatus()

    def backPropagate(self, winner):
        self.numberOfVisits += 1
        if winner == self.player:
            self.numberOfWins += 1
        if self.parent:
            self.parent.backPropagate(winner)

    def updatePossibleActions(self):
        emptySlots = [-7, -6, -5, -4, -3, -2, -1]
        for i in range(self.size):
            if self.board[i] != 0:
                emptySlots[i % 7] = i  # pour chaque colonne, on note la plus haute case non vide
        emptySlots[:] = [x + 7 for x in emptySlots if x < 35]  # si aucune case n'est remplie, emptySlots = [0,1,2,3,4,5,6]. Si > 34, on ne peut pas remplir la case du dessus
        random.shuffle(emptySlots)
        self.possibleActions = emptySlots

    def randomMove(self):
        self.updatePossibleActions()
        self.move = self.possibleActions.pop()
        self.board[self.move] = self.player
        self.player = 3-self.player

    def checkStatus(self):
        move = self.move
        board = self.board
        # check colonne
        if move > 20:
            if board[move] == board[move-7] == board[move-14] == board[move-21]:
                return board[move]
        # check diagonale gauche
        if move > 23 and move%7 > 2:
            if board[move] == board[move-8] == board[move-16] == board[move-24]:
                return board[move]
        # check diagonale droite
        if move > 20 and move%7 < 4:
            if board[move] == board[move-6] == board[move-12] == board[move-18]:
                return board[move]
        # check ligne
        start = move - min(move%7, 3)
        if move%7 < 4:
            stop = start + 1 + move%7
        else:
            stop = start + 1 + 6 - move%7
        for i in range(start, stop):
            if board[i] == board[i+1] == board[i+2] == board[i+3] != 0:
                return board[move]
        if 0 in board: #il y a encore des cases vides et aucun gagnant
            return -1
        return 0 #égalité


def bestMove(board, player):
    c = np.sqrt(2)
    root = Node(board, player=player)
    time = 600

    for t in range(time):
        node = root
        while node.childArray:
            node = node.select(c, t)
        node.updatePossibleActions()
        if node.possibleActions:
            while node.possibleActions:
                node.expand()
            randomChild = randint(0, len(node.childArray) - 1)
            child = node.childArray[randomChild]
            w = child.simulate()
        else:  # la simulation est arrivée à un noeud final qui ne peut pas être expand car toutes les cases sont remplies
            child = node
            w = child.checkStatus()
        child.backPropagate(w)

    return root.select(c, time)


if __name__ == '__main__':
    board = [0] * 42
    currentPlayer = 2

    for i in range(41): # 2 IA s'affrontent
        bestNode = bestMove(board, currentPlayer)
        board = bestNode.board
        currentPlayer = 3 - currentPlayer
        print(bestNode.checkStatus())
        if bestNode.checkStatus() != -1:
            break

    for i in range(5, -1, -1):
        print(board[0 + 7 * i: 7 + 7 * i])
    print("winner is : " + str(bestNode.checkStatus()) + ", winner move : " + str(bestNode.move))
