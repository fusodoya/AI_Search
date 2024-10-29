from search import Search, Algorithm, SearchResult

if __name__ == "__main__":
    with open('input/input-01.txt', 'r') as f:
        input_data = f.read().split('\n')

        weights = [int(i) for i in input_data[0].split(' ')]
        num_of_off_switches = len(weights)

        table = input_data[1:]
        table = [[j for j in i] for i in table]
    
    controller = Search(table, weights)
    result = controller.search(Algorithm.BFS)
    result.save_result('output-01.txt')