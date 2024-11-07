from .board_interface import BoardInterface
from .board_symbol import BoardSymbol
from .entities import Ares, Stone, EntityInterface

class DynamicBoard(BoardInterface):
    """Include Ares and stones."""
    def __init__(self, initial_board: list[list[str]], stone_weights: list):
        super().__init__(initial_board)
        
        self.__num_stones = 0
        Stone.reset()
        for h in range(self.height):
            for w in range(self.width):
                symbol = initial_board[h][w]
                if symbol == BoardSymbol.STONE_ON_SWITCH.value:
                    self._board[h][w] = Stone(is_on_switch=True, weight=stone_weights[self.__num_stones])
                    self.__num_stones += 1
                elif symbol == BoardSymbol.STONE.value:
                    self._board[h][w] = Stone(is_on_switch=False, weight=stone_weights[self.__num_stones])
                    self.__num_stones += 1
                elif symbol == BoardSymbol.ARES_ON_SWITCH.value:
                    self._board[h][w] = Ares(is_on_switch=True)
                elif symbol == BoardSymbol.ARES.value:
                    self._board[h][w] = Ares(is_on_switch=False)
                else:
                    self._board[h][w] = None  # Default for unknown symbols

        # self.__num_stones = len(stone_weights)
    
    # @property
    # def board(self) -> list[list[EntityInterface | None]]:
    #     """Copy of current board."""
    #     copied_board = super().board
    #     return copied_board
      
    def print_board(self) -> None:
        print("Dynamic board (include Ares and stones):")
        super().print_board()
        return
    
    @property
    def num_stones(self) -> int:
        return self.__num_stones