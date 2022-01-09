import random
from random import randint
from copy import deepcopy
import numpy as np
import math


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
                listUCB.append(1000000)  # on met un très grand nombre pour être sûr que cet enfant soit visité au moins une fois
            else:
                listUCB.append((child.numberOfWins / child.numberOfVisits) + c * np.sqrt(np.log(t) / child.numberOfVisits))
        return self.childArray[np.argmax(listUCB)]

    def expand(self):
        action = self.possibleActions.pop()
        childNode = Node(deepcopy(self.board), player=3-self.player, parent=self, move=action)  # si on met simplement self.board, l'enfant et le parent auront tous les 2 la même array avec 2 références différentes. La modification dans un des objets impactera l'array et cette modification sera visible dans l'autre objet
        childNode.board[action] = self.player
        self.childArray.append(childNode)
        return childNode

    def simulate(self):
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
        if move is None:  # pour le nœud root, aucun pion n'a été placé par rapport à l'état précédent
            return -1
        # check colonne
        if move > 20:
            if board[move] == board[move-7] == board[move-14] == board[move-21]:
                return board[move]
        # check diagonale /
        for i in range(move - 24, move + 1, 8):
            if (move % 7 < i % 7) or (move % 7 > (i + 24) % 7) or i < 0 or i + 24 > 41:  # une diagonale / ne peut pas commencer du côté droit du board et finir du côté gauche
                continue
            if board[i] == board[i + 8] == board[i + 16] == board[i + 24]:
                return board[move]
        # check diagonale \
        for i in range(move - 18, move + 1, 6):
            if (move % 7 > i % 7) or (move % 7 < (i + 18) % 7) or i < 0 or i + 18 > 41:  # une diagonale \ ne peut pas commencer du côté gauche du board et finir du côté droit
                continue
            if board[i] == board[i + 6] == board[i + 12] == board[i + 18]:
                return board[move]
        # check ligne
        for i in range(move - 3, move + 1):
            if (math.floor(i / 7) < math.floor(move / 7)) or (math.floor(move / 7) < math.floor((i + 3) / 7)):  # on ne vérifie que sur une même ligne de board
                continue
            if board[i] == board[i + 1] == board[i + 2] == board[i + 3]:
                return board[move]
        if 0 in board:  # il y a encore des cases vides et aucun gagnant
            return -1
        return 0  # égalité


def bestMove(board, player):
    c = np.sqrt(2)
    root = Node(board, player=player)
    time = 100

    for t in range(time):
        node = root
        while node.childArray:
            node = node.select(c, t)
        if node.checkStatus() == -1:  # le board n'est ni une victoire, ni une égalité
            node.updatePossibleActions()
            while node.possibleActions:
                node.expand()
        if len(node.childArray) != 0:  # si le nœud a des enfants, on en choisi un aléatoirement
            randomChild = randint(0, len(node.childArray) - 1)
            child = node.childArray[randomChild]
        else:
            child = node  # sinon (nœud correspondant à une victoire ou une égalité), on évalue le même nœud
        w = child.simulate()
        child.backPropagate(w)

    return root.select(c, time)


if __name__ == '__main__':
    board = [0] * 42
    currentPlayer = 2

    for i in range(41):  # 2 IA s'affrontent
        bestNode = bestMove(board, currentPlayer)
        board = bestNode.board
        currentPlayer = 3 - currentPlayer
        print(bestNode.move)
        if bestNode.checkStatus() != -1:
            break

    for i in range(5, -1, -1):
        print(board[0 + 7 * i: 7 + 7 * i])
    print("winner is : " + str(bestNode.checkStatus()) + ", winner move : " + str(bestNode.move))
