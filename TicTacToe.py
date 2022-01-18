import random
from random import randint
from copy import deepcopy
import numpy as np
import math
import matplotlib.pyplot as plt


class Node:
    def __init__(self, board, rootPlayer, player=None, parent=None, move=None):
        self.board = board
        self.player = player
        self.rootPlayer = rootPlayer
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
        childNode = Node(deepcopy(self.board), rootPlayer=self.rootPlayer, player=3 - self.player, parent=self, move=action)  # si on met simplement self.board, l'enfant et le parent auront tous les 2 la même array avec 2 références différentes. La modification dans un des objets impactera l'array et cette modification sera visible dans l'autre objet
        childNode.board[action] = childNode.player
        self.childArray.append(childNode)

    def simulate(self):
        if self.checkStatus() == 3 - self.rootPlayer:  # l'adversaire gagne avec cette board
            self.parent.numberOfWins = -1000000  # le move précédent du joueur a conduit à cette configuration. Inutile d'explorer les autres enfants car la configuartion est trop dangeureusue
        tempoNode = Node(deepcopy(self.board), rootPlayer=self.rootPlayer, player=3 - self.player, move=self.move)
        while tempoNode.checkStatus() == -1:
            tempoNode.randomMove()
        return tempoNode.checkStatus()

    def backPropagate(self, winner):
        self.numberOfVisits += 1
        if winner == self.rootPlayer:
            self.numberOfWins += 1
        if self.parent:
            self.parent.backPropagate(winner)

    def randomMove(self):
        self.updatePossibleActions()
        self.move = self.possibleActions.pop()
        self.board[self.move] = self.player
        self.player = 3-self.player

    def updatePossibleActions(self):
        emptySlots = []
        for i in range(len(board)):
            if self.board[i] == 0:
                emptySlots.append(i)
        random.shuffle(emptySlots)
        self.possibleActions = emptySlots

    def checkStatus(self):
        move = self.move
        board = self.board
        if move is None:  # pour le nœud root, aucun pion n'a été placé par rapport à l'état précédent
            return -1
        #combinaisons
        combinaisons = [[0, 1, 2],
                        [3, 4, 5],
                        [6, 7, 8],
                        [0, 3, 6],
                        [1, 4, 7],
                        [2, 5, 8],
                        [0, 4, 8],
                        [2, 4, 6]]
        for c in combinaisons:
            if board[c[0]] == board[c[1]] == board[c[2]] and board[c[0]] != 0:
                return board[c[0]]
        if 0 in board:  # il y a encore des cases vides et aucun gagnant
            return -1
        return 0  # égalité


def bestMove(board, player, time):
    c = np.sqrt(2)
    root = Node(board, rootPlayer=player, player=3-player)

    for t in range(time):
        node = root
        while node.childArray:
            node = node.select(c, t)
        if node.checkStatus() == -1:  # si le board n'est ni une victoire, ni une égalité
            node.updatePossibleActions()
            while node.possibleActions:
                node.expand()
            child = node.childArray[randint(0, len(node.childArray) - 1)]  # on choisit un enfant aléatoirement
        else:
            child = node  # sinon (nœud correspondant à une victoire ou une égalité), on évalue le même nœud
        w = child.simulate()
        child.backPropagate(w)

    return root.select(c, time)


if __name__ == '__main__':
    timeVector = np.array([10, 100, 1000, 5000])
    nbrRuns = 1000
    bilan = np.zeros(nbrRuns, dtype=int)
    bilanWin1 = np.zeros(len(timeVector), dtype=int)
    bilanWin2 = np.zeros(len(timeVector), dtype=int)
    bilanTie = np.zeros(len(timeVector), dtype=int)
    bilanVide = np.zeros(nbrRuns, dtype=int)
    bilanCasesVides = np.zeros(len(timeVector), dtype=float)

    currentPlayer = 1
    size = 9

    for i in range(len(timeVector)):
        print(timeVector[i])
        for j in range(nbrRuns):
            print("Run : " + str(j))
            board = [0] * size
            for k in range(size):  # 2 IA s'affrontent
                bestNode = bestMove(board, currentPlayer, timeVector[i])
                board = bestNode.board
                currentPlayer = 3 - currentPlayer
                #print(bestNode.move)
                if bestNode.checkStatus() != -1:
                    break
            bilan[j] = bestNode.checkStatus()
            bilanVide[j] = board.count(0)
            #print(bilan)

        bilanWin1[i] = np.count_nonzero(bilan == 1)
        bilanWin2[i] = np.count_nonzero(bilan == 2)
        bilanTie[i] = np.count_nonzero(bilan == 0)
        bilanCasesVides[i] = np.mean(bilanVide)/size

        bilan = np.zeros(nbrRuns)
        bilanVide = np.zeros(nbrRuns)



        #print(f'Pourcentage de cases vides : {np.mean(bilanCasesVides)/size}')
        #print(f'{nbrRuns} Runs à {time} itérations - victoires de 1 : {bilan.count(1)}, victoires de 2 : {bilan.count(2)}, égalités : {bilan.count(-1)}')

    print(bilanWin1, bilanWin2, bilanTie, bilanCasesVides)

    default_x_ticks = range(len(timeVector))
    plt.bar(default_x_ticks, bilanWin1, color='r', width=0.2)
    plt.bar(default_x_ticks, bilanWin2, bottom=bilanWin1, color='b', width=0.2)
    plt.bar(default_x_ticks, bilanTie, bottom=bilanWin1 + bilanWin2, color='g', width=0.2)

    plt.xlabel("Nombre d'explorations de l'arbre à partir du nœud root")
    plt.legend(["Victoires de 1", "Victoires de 2", "Égalités"])
    plt.title(f'Résultats de {nbrRuns} parties en fonction du nombre d\'explorations')
    plt.xticks(default_x_ticks, timeVector)
    plt.show()

    plt.bar(default_x_ticks, bilanCasesVides, color='black', width=0.2)
    plt.xlabel("Nombre d'explorations de l'arbre à partir du nœud root")
    plt.title(f'Pourcentage moyen du nombre de cases vides à la fin de {nbrRuns} parties')
    plt.xticks(default_x_ticks, timeVector)
    plt.show()

    #for i in range(5, -1, -1):
    #    print(board[0 + 7 * i: 7 + 7 * i])
    #print("winner is : " + str(bestNode.checkStatus()) + ", last move : " + str(bestNode.move))
