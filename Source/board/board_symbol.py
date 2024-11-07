from enum import Enum

class BoardSymbol(Enum):
    WALL = '#'
    FREE_SPACE = ' '
    STONE = '$'
    ARES = '@'
    SWITCH = '.'
    STONE_ON_SWITCH = '*'
    ARES_ON_SWITCH = '+'
    NOTHING = None