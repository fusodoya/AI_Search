from collections import deque
import heapq
from typing import Any, List, Union, Callable
from .algorithm import Algorithm
from .heuristics import Heuristics

class SearchFrontier:
    def __init__(self, algorithm: Algorithm):
        if not isinstance(algorithm, Algorithm):
            raise ValueError(f"Unsupported algorithm: {algorithm}")

        self.__algorithm = algorithm
        self.frontier: Union[List[Any], deque] = self.__initialize_frontier()
        self._add_func: Callable[[Any], None] = self.__get_add_function()
        self._pop_func: Callable[[], Any] = self.__get_pop_function()

    def __initialize_frontier(self) -> Union[List[Any], deque]:
        if self.__algorithm == Algorithm.DFS:
            return []  # Stack for DFS
        elif self.__algorithm == Algorithm.BFS:
            return deque()  # Queue for BFS
        else:
            return []  # List for UCS and A*
        
    @property
    def algorithm(self) -> Algorithm:
        return self.__algorithm
    
    def add(self, item: Any) -> None:
        self._add_func(item)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("Pop from an empty frontier.")
        
        return self._pop_func()

    def is_empty(self) -> bool:
        return len(self.frontier) == 0

    def peek(self) -> Any:
        if self.is_empty():
            return None
        
        if self.__algorithm == Algorithm.DFS:
            return self.frontier[-1]  # Peek at the top of the stack
        elif self.__algorithm == Algorithm.BFS:
            return self.frontier[0]  # Peek at the front of the queue
        elif self.__algorithm == Algorithm.UCS:
            return self.frontier[0]  # Peek at the front of the queue
        else:
            return self.frontier[0]  # Peek at the top of the priority queue
        
    def __get_add_function(self) -> Callable[[Any], None]:
        if self.__algorithm == Algorithm.DFS:
            return self._add_dfs
        elif self.__algorithm == Algorithm.BFS:
            return self._add_bfs
        elif self.__algorithm == Algorithm.UCS:
            return self._add_ucs
        else: 
            return self._add_a_star

    def __get_pop_function(self) -> Callable[[], Any]:
        if self.__algorithm == Algorithm.DFS:
            return self._pop_dfs
        elif self.__algorithm == Algorithm.BFS:
            return self._pop_bfs
        elif self.__algorithm == Algorithm.UCS:
            return self._pop_ucs
        else:
            return self._pop_a_star

    # Add
    def _add_dfs(self, item: Any) -> None:
        self.frontier.append(item)  # Push onto stack

    def _add_bfs(self, item: Any) -> None:
        self.frontier.append(item)  # Enqueue for BFS

    def _add_ucs(self, item: Any) -> None:
        heapq.heappush(self.frontier, item)  # Push into priority queue

    def _add_a_star(self, item: Any) -> None:
        heapq.heappush(self.frontier, (item[0] + Heuristics.cal(item[1]), item))  # Push into priority queue

    # Pop
    def _pop_dfs(self) -> Any:
        return self.frontier.pop()  # Pop from stack

    def _pop_bfs(self) -> Any:
        return self.frontier.popleft()  # Dequeue from BFS

    def _pop_ucs(self) -> Any:
        return heapq.heappop(self.frontier)  # Pop from priority queue

    def _pop_a_star(self) -> None:
        return heapq.heappop(self.frontier)[1]  # Pop from priority queue