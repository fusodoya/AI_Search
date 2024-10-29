from abc import ABC, abstractmethod
from .board_symbol import BoardSymbol

class BoardInterface(ABC):
    def __init__(self, initial_board: list[list[str]]):
        super().__init__()

        try:
            # Validate the structure of the provided board
            self.__validate_board_structure(initial_board)
        except (TypeError, ValueError) as e:
            print(f"Board validation error: {e}")
            raise
        
        self.__height = len(initial_board)
        self.__width = len(initial_board[0]) if self.__height > 0 else 0
        
        # Create a deep copy of the board after validation
        self._board = self.__copy_board(initial_board)
    
    @property
    def height(self) -> int:
        """Height of the board."""
        return self.__height
    
    @property
    def width(self) -> int:
        """Width of the board."""
        return self.__width
    
    @property
    def board(self) -> list[list[str]]:
        """Copy of current board."""
        copied_board = self.__copy_board(self._board)
        return copied_board
    
    @abstractmethod
    def print_board(self) -> None:
        """Print the current state of the board."""
        for row in self._board:
            print(row)
        return

    def __copy_board(self, board: list[list[str]]) -> list[list[str]]:
        # Create a deep copy of the board
        return [row[:] for row in board]

    def __validate_board_structure(self, board: list[list[str]]) -> None:
        """Ensure the provided board is a valid structure.
        
            Raise:
                TypeError: if the board is not a list
                ValueError: if the board has inconsistent row lengths"""
        
        if not isinstance(board, list):
            raise TypeError("The board must be a list.")
        
        if len(board) == 0:
            return
        
        if any(not isinstance(row, list) for row in board):
            raise TypeError("Each row in the board must be a list.")
        
        width = len(board[0])
        if any(len(row) != width for row in board):
            raise ValueError("All rows in the board must have the same width.")
        
        valid_symbols = {symbol.value for symbol in BoardSymbol}
        for row in board:
            if any(element not in valid_symbols for element in row):
                raise ValueError(f"Invalid value in the board. Must be one of {valid_symbols}.")
        return
