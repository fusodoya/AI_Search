from board import StaticBoard, DynamicBoard, BoardSymbol
from .search_frontier import Algorithm, SearchFrontier

class Search:
    def __init__(self, initial_board: list[list[str]], stone_weights: list):
        self.__static_board = StaticBoard(initial_board)
        self.__dynamic_board = DynamicBoard(initial_board, stone_weights)
        self.__num_stones = self.__dynamic_board.num_stones
        
    def print_info(self):
        self.__static_board.print_board()
        self.__dynamic_board.print_board()
    
    def search(self, algorithm: Algorithm):
        self.visited_states = {}
        self.trade = {}

        # save position of entities
        self.entity_positions = [(0, 0) for _ in range(self.__num_stones + 1)]
        for i in range(self.__dynamic_board.height):
            for j in range(self.__dynamic_board.width):
                entity = self.__dynamic_board.board[i][j]
                if entity is not None:
                    self.entity_positions[entity.id] = (i, j)

        # save the state
        hash_code = tuple(self.entity_positions)
        self.visited_states[hash_code] = True
        
        
        self.trade[hash_code] = ((-1, -1), (-1, -1))
        self.warehouse = SearchFrontier(algorithm)
        self.warehouse.add(hash_code)

        dx = [-1, 0, 1, 0]
        dy = [0, 1, 0, -1]
        
        while (True):
            self.final_state = self.warehouse.pop()
            cnt = 0
            stone_checker = set()
            for i in range(self.__num_stones):
                stone_pos = self.final_state[i + 1]
                cnt += (self.__static_board.board[stone_pos[0]][stone_pos[1]] == BoardSymbol.SWITCH.value)
                stone_checker.add(stone_pos)
            if (cnt == self.__num_stones):
                break

            current_state = list(self.final_state)
            Ares_pos = current_state[0]
            for i in range(4):
                x = Ares_pos[0] + dx[i]
                y = Ares_pos[1] + dy[i]

                new_state = list(current_state)
                if ((x, y) in stone_checker): # Co da tai vi tri (x, y)
                    if ((x + dx[i], y + dy[i]) in stone_checker
                    or self.__static_board.board[x + dx[i]][y + dy[i]] == BoardSymbol.WALL.value):
                        continue
                    else:
                        idx = current_state.index((x, y))
                        new_state[idx] = (x + dx[i], y + dy[i])
                        new_state[0] = (x, y)
                        stone_checker.remove((x, y))
                        stone_checker.add((x + dx[i], y + dy[i]))
                else:
                    if (self.__static_board.board[x][y] == BoardSymbol.WALL.value):
                        continue
                    new_state[0] = (x, y)
                
                hash_code = tuple(new_state)
                if (not self.visited_states.get(hash_code, False)):
                    self.visited_states[hash_code] = True
                    self.trade[hash_code] = self.final_state
                    self.warehouse.add(hash_code)

        ways = ''
        current_state = self.final_state
        while (True):
            prev_state = self.trade[current_state]
            if (prev_state[0] == (-1, -1)):
                break

            is_push = False
            for i in range(self.__num_stones):
                if (prev_state[i + 1] != current_state[i + 1]):
                    is_push = True
                    break
            
            move_code = self.__find_move_code(prev_state[0], current_state[0])
            if (is_push):
                move_code = move_code.upper()

            ways += move_code
            current_state = prev_state
        ways = ways[::-1]
        
        return ways
    
    def __find_move_code(self, prev_pos, current_pos) -> str:
        if (current_pos[0] - prev_pos[0] == 1):
            return 'd'
        if (current_pos[0] - prev_pos[0] == -1):
            return 'u'
        if (current_pos[1] - prev_pos[1] == 1):
            return 'r'
        return 'l'