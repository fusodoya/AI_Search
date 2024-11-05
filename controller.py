from search.search_result import SearchResult
from search.search import Search
from search.algorithm import Algorithm

class Controller:
    def __init__(self, test_id: str):
        while (len(test_id) < 2):
            test_id = '0' + test_id
        self.inp_dir = 'input/input-' + test_id + '.txt'
        self.out_dir = 'output/output-' + test_id + '.txt'

        with open(self.inp_dir, 'r') as inpstream:
            input_data = inpstream.read().split('\n')

            weights = [int(i) for i in input_data[0].split(' ')]
            num_of_off_switches = len(weights)

            table = input_data[1:]
            table = [[j for j in i] for i in table]

            width = 0
            for row in table:
                width = max(width, len(row))

            for row in table:
                for i in range(width - len(row)):
                    row.append(' ')
            
        self.controller = Search(table, tuple(weights))
    
    def run(self):
        with open(self.out_dir, 'w') as outstream:
            result = self.controller.search(Algorithm.BFS)
            result.save_result(outstream)

            result = self.controller.search(Algorithm.DFS)
            result.save_result(outstream)

            result = self.controller.search(Algorithm.UCS)
            result.save_result(outstream)

            result = self.controller.search(Algorithm.A_STAR)
            result.save_result(outstream)

    def exec(self, algorithm: Algorithm):
        pass