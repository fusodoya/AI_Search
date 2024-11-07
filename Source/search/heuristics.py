from board import StaticBoard, BoardSymbol
from .algorithm import Algorithm
from collections import deque


class Heuristics:
    def __init__(self, static_board: StaticBoard, stone_weights: tuple):
        self.__inf = 9999 * static_board.height * static_board.width
        switch_position = []
        for i in range(static_board.height):
            for j in range(static_board.width):
                if (static_board.board[i][j] == BoardSymbol.SWITCH.value):
                    switch_position.append((i, j))

        self.__switch_position = tuple(switch_position)
        self.__num_switchs = len(self.__switch_position)
        self.__stone_weights = stone_weights
        self.__num_stones = len(self.__stone_weights)

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
        
        self.__table = [[0 
            for _ in range(self.__num_stones + 1)]
            for _ in range(self.__num_switchs + 1)]
        
    def calculate(self, state: tuple) -> int:
        for i in range(self.__num_switchs):
            for j in range(self.__num_stones):
                (x, y) = state[j + 1]
                self.__table[i + 1][j + 1] = self.__shortest_distance[i][x][y] * self.__stone_weights[j]

        switch_val = [0 for _ in range(self.__num_switchs + 1)]
        stone_val = [0 for _ in range(self.__num_stones + 1)]
        matchs = [0 for _ in range(self.__num_stones + 1)]
        way = [0 for _ in range(self.__num_stones + 1)]

        for i in range(1, self.__num_switchs + 1):
            matchs[0] = i
            j_tmp = 0
            minv = [self.__inf for _ in range(self.__num_stones + 1)]
            used = [False for _ in range(self.__num_stones + 1)]

            while (True):
                used[j_tmp] = True
                i_tmp = matchs[j_tmp]
                delta = self.__inf
                j_run = 0

                for j in range(1, self.__num_stones + 1):
                    if (not used[j]):
                        cur = self.__table[i_tmp][j] - switch_val[i_tmp] - stone_val[j]
                        if (cur < minv[j]):
                            minv[j] = cur
                            way[j] = j_tmp
                        if (minv[j] < delta):
                            delta = minv[j]
                            j_run = j
                for j in range(self.__num_switchs + 1):
                    if (used[j]):
                        switch_val[matchs[j]] += delta
                        stone_val[j] -= delta
                    else:
                        minv[j] -= delta
                j_tmp = j_run
                
                if (matchs[j_tmp] == 0):
                    break
            
            while (True):
                j_run = way[j_tmp]
                matchs[j_tmp] = matchs[j_run]
                j_tmp = j_run
                if (j_tmp == 0):
                    break

        return -stone_val[0]
