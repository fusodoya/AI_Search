from board.board_interface import BoardInterface
from board.board_symbol import BoardSymbol

class StaticBoard(BoardInterface):
    """Include wall, free space, and switch."""
    def __init__(self, initial_board: list[list[str]]):
        super().__init__(initial_board)
        for h in range(self.height):
            for w in range(self.width):
                if self.board[h][w] in {BoardSymbol.SWITCH.value,
                BoardSymbol.STONE_ON_SWITCH.value, 
                BoardSymbol.ARES_ON_SWITCH.value}:
                    self.board[h][w] = BoardSymbol.SWITCH.value
                elif (self.board[h][w] != BoardSymbol.WALL.value):
                    self.board[h][w] = BoardSymbol.FREE_SPACE.value
    
    def print_board(self) -> None:
        print("Static board (include wall, free space, and switch):")
        super().print_board()
        return