import sys
import os

from board_folder.object_val import *

class ConstBoard:
    def __init__(self, table):
        self.height = len(table)
        self.width = len(table[0])

        self.board = [[FREE_SPACE for _ in range(self.width)] for _ in range(self.height)]
        
        for i in range(self.height):
            for j in range(self.width):
                if (table[i][j] == WALL or table[i][j] == SWITCH):
                    self.board[i][j] = table[i][j]

    def print_info(self):
        print("Const Board (include wall, free space, and switch):")
        for i in range(self.height):
            print(self.board[i])
        print("")

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width
        
    