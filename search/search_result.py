from .search_frontier import Algorithm

class SearchResult:
    def __init__(self, type: Algorithm, step: int, weight: int, node: int, time: float, memory: float, ways: str):
        self.__type = type
        self.__step = step
        self.__weight = weight
        self.__node = node
        self.__time = time
        self.__memory = memory
        self.__ways = ways
    
    def save_result(self, file_path: str):
        with open(file_path, 'w') as outstream:
            outstream.write(f"{self.__type.name}\n")
            outstream.write(f"Steps: {self.__step}, ")
            outstream.write(f"Weight: {self.__weight}, ")
            outstream.write(f"Node: {self.__node}, ")
            outstream.write(f"Time (ms): {self.__time:.3f}, ")
            outstream.write(f"Memory (MB): {self.__memory:.3f}\n")
            outstream.write(f"{self.__ways}\n")