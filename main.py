from search import Search, Algorithm, SearchResult

def test(test_id: str, algorithm: Algorithm):
    while (len(test_id) < 2):
        test_id = '0' + test_id
    inp_dir = 'input/input-' + test_id + '.txt'
    out_dir = 'output/output-' + test_id + '.txt'

    with open(inp_dir, 'r') as f:
        input_data = f.read().split('\n')

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
    
        controller = Search(table, tuple(weights))
        result = controller.search(algorithm)
        result.save_result(out_dir)

if __name__ == "__main__":

    test(str(10), Algorithm.A_STAR)
    # for i in range(1, 8):
    #     test(str(i))