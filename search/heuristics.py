from board import StaticBoard, BoardSymbol
from .algorithm import Algorithm
from collections import deque


class Heuristics:
    def __init__(self, static_board: StaticBoard):
        self.__inf = 9999 * static_board.height * static_board.width
        switch_position = []
        for i in range(static_board.height):
            for j in range(static_board.width):
                if (static_board.board[i][j] == BoardSymbol.SWITCH.value):
                    switch_position.append((i, j))

        self.__switch_position = tuple(switch_position)
        self.__num_switchs = len(self.__switch_position)

        self.__shortest_distance = [[[self.__inf 
            for _ in range(static_board.width)]
            for _ in range(static_board.height)]
            for _ in range(self.__num_switchs)]

        self.warehouse = deque()
        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]

        for idx in range(self.__num_switchs):
            (x, y) = self.__switch_position[idx]
            self.warehouse.append((x, y))
            self.__shortest_distance[idx][x][y] = 0

            while (len(self.warehouse) > 0):
                (x, y) = self.warehouse.popleft()
                for i in range(4):
                    newX = x + dx[i]
                    newY = y + dy[i]
                    if (static_board.board[newX][newY] != BoardSymbol.WALL.value
                    and self.__shortest_distance[idx][newX][newY] == self.__inf):
                        self.__shortest_distance[idx][newX][newY] =  self.__shortest_distance[idx][x][y] + 1
                        self.warehouse.append((newX, newY))
        
    def heuristics(self, status: tuple) -> int:
        return 0