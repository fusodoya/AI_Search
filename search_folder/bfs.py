from search_folder.search import *
from object_folder.ares import *
from object_folder.stone import *
from collections import deque


class BFS(Search):
    def __init__(self, table, weights):
        super().__init__(table, weights)
        pass

    def print_info(self):
        super().print_info()

    def find(self):
        self.checker = {}
        self.trade = {}

        self.state = [(0, 0) for _ in range(Stone.cnt + 1)]
        for i in range(self.const_board.get_height()):
            for j in range(self.const_board.get_width()):
                if (self.object_board.board[i][j] != None):
                    self.state[self.object_board.board[i][j].id] = (i, j)

        hash_code = tuple(self.state)
        self.checker[hash_code] = True
        self.trade[hash_code] = ((-1, -1), (-1, -1))
        self.warehouse = deque()
        self.warehouse.append(hash_code)

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        while (True):
            self.final_state = self.warehouse.popleft() # Neu ma PP search khac, thi thay DS voi thay pop la ok
            cnt = 0
            stone_checker = set()
            for i in range(Stone.cnt):
                stone_pos = self.final_state[i + 1]
                cnt += (self.const_board.board[stone_pos[0]][stone_pos[1]] == SWITCH)
                stone_checker.add(stone_pos)
            if (cnt == Stone.cnt):
                break

            current_state = list(self.final_state)
            Ares_pos = current_state[0]
            for i in range(4):
                x = Ares_pos[0] + dx[i]
                y = Ares_pos[1] + dy[i]

                new_state = list(current_state)
                if ((x, y) in stone_checker): # Co da tai vi tri (x, y)
                    if ((x + dx[i], y + dy[i]) in stone_checker
                    or self.const_board.board[x + dx[i]][y + dy[i]] == WALL):
                        continue
                    else:
                        idx = current_state.index((x, y))
                        new_state[idx] = (x + dx[i], y + dy[i])
                        new_state[0] = (x, y)
                        stone_checker.remove((x, y))
                        stone_checker.add((x + dx[i], y + dy[i]))
                else:
                    if (self.const_board.board[x][y] == WALL):
                        continue
                    new_state[0] = (x, y)
                
                hash_code = tuple(new_state)
                if (not self.checker.get(hash_code, False)):
                    self.checker[hash_code] = True
                    self.trade[hash_code] = self.final_state
                    self.warehouse.append(hash_code)

        ways = []
        current_state = self.final_state
        while (True):
            if (current_state[0] == (-1, -1)):
                break
            ways.append(current_state[0])
            current_state = self.trade[current_state]
        ways = list(reversed(ways))
        return ways