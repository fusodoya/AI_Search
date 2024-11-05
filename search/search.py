from board import StaticBoard, DynamicBoard, BoardSymbol
from .search_frontier import SearchFrontier
from .algorithm import Algorithm
from .search_result import SearchResult
from .heuristics import Heuristics
import time
import resource

class Search:
    def __init__(self, initial_board: list[list[str]], stone_weights: list):
        self.__static_board = StaticBoard(initial_board)
        self.__dynamic_board = DynamicBoard(initial_board, stone_weights)
        self.__num_stones = self.__dynamic_board.num_stones
        self.__stone_weights = stone_weights
        self.__heuristic_calculator = Heuristics(self.__static_board)
        
    def print_info(self):
        self.__static_board.print_board()
        self.__dynamic_board.print_board()
    
    def search(self, algorithm: Algorithm) -> SearchResult:
        __start_time = time.time()
        __mem_before = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        self.min_steps = {}
        self.trade = {}
        # self.virtualWall = [[False for _ in range(self.__static_board.width)] for _ in range(self.__static_board.height)]

        # save position of entities
        self.entity_positions = [(0, 0) for _ in range(self.__num_stones + 1)]
        for i in range(self.__dynamic_board.height):
            for j in range(self.__dynamic_board.width):
                entity = self.__dynamic_board.board[i][j]
                if entity is not None:
                    self.entity_positions[entity.id] = (i, j)

        # save the state
        hash_code = tuple(self.entity_positions)
        __weight = 0
        __step = 0
        self.min_steps[hash_code] = __step
        
        self.trade[hash_code] = ((-1, -1), (-1, -1))
        self.warehouse = SearchFrontier(algorithm)
        self.warehouse.add(((__weight, __step), hash_code))

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        
        __node = 0
        while (True):
            if (self.warehouse.is_empty()):
                return SearchResult(algorithm)
            self.final_state = self.warehouse.pop()
            (__weight, __step) = self.final_state[0]

            optimize_step = self.min_steps.get(self.final_state[1])
            if (__step != optimize_step):
                self.warehouse.add(((__weight, optimize_step), self.final_state[1]))
                continue

            __node += 1
            num_stones_in_switch = 0
            self.stone_checker = set()
            for i in range(self.__num_stones):
                stone_pos = self.final_state[1][i + 1]
                num_stones_in_switch += (self.__static_board.board[stone_pos[0]][stone_pos[1]] == BoardSymbol.SWITCH.value)
                self.stone_checker.add(stone_pos)
                
            if (num_stones_in_switch == self.__num_stones):
                break

            # if (self.__advance_check()):
            #     continue
            
            current_state = list(self.final_state[1])
            Ares_pos = current_state[0]
            new_step = __step + 1

            for i in range(4):
                new_weight = __weight
                x = Ares_pos[0] + dx[i]
                y = Ares_pos[1] + dy[i]

                new_state = list(current_state)
                if ((x, y) in self.stone_checker): # Co da tai vi tri (x, y)
                    if ((x + dx[i], y + dy[i]) in self.stone_checker
                    or self.__static_board.board[x + dx[i]][y + dy[i]] == BoardSymbol.WALL.value):
                        continue
                    else:
                        stone_pos = (x + dx[i], y + dy[i])
                        if (self.__static_board.board[stone_pos[0]][stone_pos[1]] != BoardSymbol.SWITCH.value):
                            if (self.__is_corner(stone_pos)):
                                continue
                      
                        new_state[0] = (x, y)

                        idx = current_state.index((x, y))
                        new_weight += self.__stone_weights[idx - 1]
                        new_state[idx] = stone_pos
                        self.stone_checker.remove((x, y))
                        self.stone_checker.add(stone_pos)
                else:
                    if (self.__static_board.board[x][y] == BoardSymbol.WALL.value):
                        continue
                    new_state[0] = (x, y)
                
                hash_code = tuple(new_state)

                current_step = self.min_steps.get(hash_code, -1)
                if (current_step == -1):
                    self.min_steps[hash_code] = new_step
                    self.trade[hash_code] = self.final_state[1]
                    self.warehouse.add(((new_weight, new_step), hash_code))
                elif (new_step < current_step):
                    self.min_steps[hash_code] = new_step
                    self.trade[hash_code] = self.final_state[1]

        ways = ''
        current_state = self.final_state[1]
        while (True):
            prev_state = self.trade[current_state]
            if (prev_state[0] == (-1, -1)):
                break

            is_push = 0
            for i in range(self.__num_stones):
                if (prev_state[i + 1] != current_state[i + 1]):
                    is_push = i + 1
                    break
            
            move_code = self.__find_move_code(prev_state[0], current_state[0], is_push)
            ways += move_code
            current_state = prev_state
        
        ways = ways[::-1]
        
        __end_time = time.time()
        __mem_after = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

        __time = (__end_time - __start_time) * 1000
        __memory = (__mem_after - __mem_before) / 1024
        
        return SearchResult(algorithm, __step, __weight, __node, __time, __memory, ways)
    
    def __find_move_code(self, prev_pos, current_pos, is_push) -> str:
        if current_pos[0] - prev_pos[0] == 1:
            move_code = 'd'
        elif current_pos[0] - prev_pos[0] == -1:
            move_code = 'u'
        elif current_pos[1] - prev_pos[1] == 1:
            move_code = 'r'
        else:
            move_code = 'l'
        
        if (is_push != 0):
            move_code = move_code.upper()
            
        return move_code
    
    def __is_corner(self, pos: tuple) -> bool:
        (x, y) = pos
        return ((self.__static_board.board[x + 1][y] == BoardSymbol.WALL.value
        or self.__static_board.board[x - 1][y] == BoardSymbol.WALL.value)
        and
        (self.__static_board.board[x][y + 1] == BoardSymbol.WALL.value
        or self.__static_board.board[x][y - 1] == BoardSymbol.WALL.value))

    # Advance update
    def __advance_check(self):
        for i in range(self.__num_stones):
            stone_pos = self.final_state[1][i + 1]

            if (self.__is_horizon_wall(stone_pos)):
                if (self.__dead_block_horizon(stone_pos)):
                    return True
            if (self.__is_vertical_wall(stone_pos)):
                if (self.__dead_block_vertical(stone_pos)):
                    return True
        return False

    def __is_horizon_wall(self, pos: tuple) -> bool:
        (x, y) = pos
        return (self.__static_board.board[x][y + 1] == BoardSymbol.WALL.value
        or self.__static_board.board[x][y - 1] == BoardSymbol.WALL.value
        or self.virtualWall[x][y + 1]
        or self.virtualWall[x][y - 1])

    def __is_vertical_wall(self, pos: tuple) -> bool:
        (x, y) = pos
        return (self.__static_board.board[x + 1][y] == BoardSymbol.WALL.value
        or self.__static_board.board[x - 1][y] == BoardSymbol.WALL.value
        or self.virtualWall[x + 1][y]
        or self.virtualWall[x - 1][y])

    def __dead_block_horizon(self, pos: tuple) -> bool:
        (x, y) = pos
        self.virtualWall[x][y] = True

        nearStone = (x + 1, y)
        if (nearStone in self.stone_checker):
            if (self.__is_horizon_wall(nearStone)):
                self.virtualWall[x][y] = False
                return True
            if (self.__dead_block_vertical(nearStone)):
                self.virtualWall[x][y] = False
                return True

        nearStone = (x - 1, y)
        if (nearStone in self.stone_checker):
            if (self.__is_horizon_wall(nearStone)):
                self.virtualWall[x][y] = False
                return True
            if (self.__dead_block_vertical(nearStone)):
                self.virtualWall[x][y] = False
                return True
        
        self.virtualWall[x][y] = False
        return False

    def __dead_block_vertical(self, pos: tuple) -> bool:
        (x, y) = pos
        self.virtualWall[x][y] = True

        nearStone = (x, y + 1)
        if (nearStone in self.stone_checker):
            if (self.__is_vertical_wall(nearStone)):
                self.virtualWall[x][y] = False
                return True
            if (self.__dead_block_horizon(nearStone)):
                self.virtualWall[x][y] = False
                return True

        nearStone = (x, y - 1)
        if (nearStone in self.stone_checker):
            if (self.__is_vertical_wall(nearStone)):
                self.virtualWall[x][y] = False
                return True
            if (self.__dead_block_horizon(nearStone)):
                self.virtualWall[x][y] = False
                return True
        
        self.virtualWall[x][y] = False
        return False
        
        

        
        