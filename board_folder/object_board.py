from board_folder.object_val import *
from object_folder.ares import *
from object_folder.stone import *

class ObjectBoard:
    def __init__(self, table, weights):
        self.__height = len(table)
        self.__width = len(table[0])

        self.__board = [[None for _ in range(self.__width)] for _ in range(self.__height)]
        
        for i in range(self.__height):
            for j in range(self.__width):
                if (table[i][j] == STONE):
                    self.__board[i][j] = Stone(weights[Stone.cnt], table[i][j] == SWITCH)
                if (table[i][j] == ARES):
                    self.__board[i][j] = Ares(table[i][j] == SWITCH)

    def print_info(self):
        print("Const Board (include Ares and box):")
        for i in range(self.__height):
            print(self.__board[i])
        print("")

        for i in range(self.__height):
            for j in range(self.__width):
                if (self.__board[i][j] != None):
                    self.__board[i][j].print_info()
    