from abc import ABC, abstractmethod
from board_folder.const_board import *
from board_folder.object_board import *

class Search(ABC):
    def __init__(self, table, weights):
        self.const_board = ConstBoard(table)
        self.object_board = ObjectBoard(table, weights)

    def print_info(self):
        self.const_board.print_info()
        self.object_board.print_info()
