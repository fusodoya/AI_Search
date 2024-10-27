from board_folder.object_val import *
from object_folder.ares import *
from object_folder.stone import *

class ObjectBoard:
    def __init__(self, table, weights):
        self.height = len(table)
        self.width = len(table[0])
        self.correct_stone = 0

        self.board = [[None for _ in range(self.width)] for _ in range(self.height)]
        
        for j in range(self.width):
            for i in range(self.height):
                if (table[i][j] == STONE):
                    self.board[i][j] = Stone(weights[Stone.cnt], False)
                if (table[i][j] == STONE_ON_SWITCH):
                    self.board[i][j] = Stone(weights[Stone.cnt], True)
                    self.correct_stone += 1
                if (table[i][j] == ARES):
                    self.board[i][j] = Ares(False)
                if (table[i][j] == ARES_ON_SWITCH):
                    self.board[i][j] = Ares(True)

    def print_info(self):
        print("Const Board (include Ares and box):")
        for i in range(self.height):
            print(self.board[i])
        print("")

        for i in range(self.height):
            for j in range(self.width):
                if (self.board[i][j] != None):
                    print("(" + str(i) + ", " + str(j) + ")")
                    self.board[i][j].print_info()
    