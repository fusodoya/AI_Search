from search_folder.bfs import *

if __name__ == "__main__":
    with open('input/input-01.txt', 'r') as f:
        input_data = f.read().split('\n')

        weights = [int(i) for i in input_data[0].split(' ')]
        num_of_off_switches = len(weights)

        table = input_data[1:]
        table = [[j for j in i] for i in table]

    n = len(table)
    for i in range(n):
            print(table[i])
    print(len(table))
    print(len(table[0]))
    print(weights)

    Controller = BFS(table, weights)
    Controller.print_info()