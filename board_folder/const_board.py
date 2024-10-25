import sys
import os

from board_folder.object_val import *

class ConstBoard:
    def __init__(self, table):
        self.__height = len(table)
        self.__width = len(table[0])

        self.__board = [[FREE_SPACE for _ in range(self.__width)] for _ in range(self.__height)]
        
        for i in range(self.__height):
            for j in range(self.__width):
                if (table[i][j] == WALL or table[i][j] == SWITCH):
                    self.__board[i][j] = table[i][j]

    def print_info(self):
        print("Const Board (include wall, free space, and switch):")
        for i in range(self.__height):
            print(self.__board[i])
        print("")

        
    