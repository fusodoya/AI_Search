from collections import deque
import heapq
from enum import Enum
from typing import Any, List, Union, Callable

class Algorithm(Enum):
    DFS = 1
    BFS = 2
    UCS = 3
    A_STAR = 4

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
        else:  # UCS or A*
            return self.frontier[0]  # Peek at the top of the priority queue
        
    def __get_add_function(self) -> Callable[[Any], None]:
        if self.__algorithm == Algorithm.DFS:
            return self._add_dfs
        elif self.__algorithm == Algorithm.BFS:
            return self._add_bfs
        else:  # UCS or A*
            return self._add_priority

    def __get_pop_function(self) -> Callable[[], Any]:
        if self.__algorithm == Algorithm.DFS:
            return self._pop_dfs
        elif self.__algorithm == Algorithm.BFS:
            return self._pop_bfs
        else:  # UCS or A*
            return self._pop_priority

    def _add_dfs(self, item: Any) -> None:
        self.frontier.append(item)  # Push onto stack

    def _add_bfs(self, item: Any) -> None:
        self.frontier.append(item)  # Enqueue for BFS

    def _add_priority(self, item: Any) -> None:
        heapq.heappush(self.frontier, item)  # Push into priority queue

    def _pop_dfs(self) -> Any:
        return self.frontier.pop()  # Pop from stack

    def _pop_bfs(self) -> Any:
        return self.frontier.popleft()  # Dequeue from BFS

    def _pop_priority(self) -> Any:
        return heapq.heappop(self.frontier)  # Pop from priority queue

