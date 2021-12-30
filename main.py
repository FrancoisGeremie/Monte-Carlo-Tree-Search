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


class Node:
    def __init__(self, value, parent):
        self.value = value
        self.parent = parent
        self.childArray = []

    def addChildrens(self, value):
        self.childArray.append(Node(value, self.value))



if __name__ == '__main__':
    jeu = Board(4)
    jeu.updateBoard(1,0)
    #print(jeu.checkStatus())
    root = Node(2, None)
    root.addChildrens(6)
    root.addChildrens(4)
    print(root.value)
    print(root.childArray[0].value)

