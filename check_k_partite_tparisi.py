#!/usr/bin/python3
import k_partite_matching_tparisi as match
import generate_graphs_tparisi as gen

'''Runs k_partite_matching_tparisi.py on the dataset testing_graphs/check_test_data_tparisi.csv
- This dataset was input manually and contains 6 data sets:
1. bipartite graph (solveable)
2. bipartite graph (not solveable)
3. 3-partite graph (solveable)
4. 3-partite graph (not solveable)
5. 4-partite graph (solveable)
6. 4-partite graph (not solveable)
Checks to make sure the algorithm generates correct answers to these problems'''

def check_algorithm(filename):
    graphs = gen.load_from_file(filename)
    correct = True
    for num, G in enumerate(graphs, start=1):
        result = match.solve(G, G.graph["k"])
        if result != correct:
            print(f"ERROR: k-partite matching incorrect on graph #{num}")
        else:
            print(f'Graph #{num} correct!')
        correct = not correct
        
    
def main():
    check_algorithm('testing_graphs/check_test_data_tparisi.csv')

if __name__ == '__main__':
    main()