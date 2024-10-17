import networkx as nx
import random
import csv

### GLOBALS
GRAPHS_PER_SIZE = 15

### FUNCTIONS
def generate_graph(num_nodes, edge_quantity):
    '''Generates a graph with n_nodes and random edges (up to edge_quantity)'''
    g1 = nx.Graph()
    g1.add_nodes_from(list(range(num_nodes)))
    non_edges = list(nx.non_edges(g1))
    for _ in range(edge_quantity):
        if not non_edges:
            break
        next_edge = non_edges[random.randint(0, len(non_edges)-1)]
        g1.add_edge(next_edge[0], next_edge[1])
    return g1
        
def full_graph(n):
    '''Generates graph where every node is fully connected to all other nodes'''
    graph = nx.Graph()
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            graph.add_edge(i, j)
    return graph

def load_from_file(filepath):
    '''Loads a .csv file in the specified CNF format and returns the corresponding graphs
    (Assumes graphs are not directed/weighted)
    Header should be formatted as follows:
    c,x,y,z where
    x = problem number
    y = k number for matching
    z = True/false (is the graph satisfiable)'''
    graphs = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if not row:
                continue
            header = row.pop(0)
            if header == 'c':
                graph = nx.Graph(k=int(row[1]))
                graphs.append(graph)
            elif header == 'p':
                vertices = int(row[1])
                edges = int(row[2])
            elif header == 'e':
                edges -= 1
                graph.add_edge(row[0], row[1])
            elif header == 'v':
                vertices -= 1
                graph.add_node(row[0])
    if edges != 0 or vertices != 0:
        print("ERROR: Incorrect header")
        return None
    return graphs

def save_to_file(g1, filename, num, k, value=None):
    '''Saves a provided graph to file in the specified CNF format
    g1: graph to be saved
    filename: filename where graph is to be saved
    num: '''
    with open(filename, 'a') as file:
        if value:
            file.write(f'c,{num},{k},{value}\n')
        else:
            file.write(f'c,{num},{k}\n')
        file.write(f'p,u,{len(g1.nodes)},{len(g1.edges)}\n')
        for node in g1.nodes():
            file.write(f'v,{node}\n')
        for edge in g1.edges():
            file.write(f'e,{edge[0]},{edge[1]}\n')
            
def save_to_open_file(g1, file, num, k, value=None):
    '''Saves a provided graph to file in the specified CNF format
    g1: graph to be saved
    filename: filename where graph is to be saved
    num: '''
    if value:
        file.write(f'c,{num},{k},{value}\n')
    else:
        file.write(f'c,{num},{k}\n')
    file.write(f'p,u,{len(g1.nodes)},{len(g1.edges)}\n')
    for node in g1.nodes():
        file.write(f'v,{node}\n')
    for edge in g1.edges():
        file.write(f'e,{edge[0]},{edge[1]}\n')

def manual_graph_gen(filename, graph_num):
    '''Prompts user for values manually and generates graphs based on data'''
    for ix in range(graph_num):
        while True:
            try:
                nodes = input("How many nodes do you want? ")
                edges = input("How many edges do you want? ")
                k = input("What k-value do you want for this graph? ")
                nodes = int(nodes)
                edges = int(edges)
                k = int(k)
                break
            except:
                print("Sorry, I couldn't read one of those numbers. Please try again")
        print(f'Saving to {filename}...')
        save_to_file(generate_graph(nodes, edges), filename, ix, k)      

def auto_graph_gen(filename, graph_num, k=0):
    '''Genrates graphs automatically based on k-value'''
    if k == 0:
        while True:
                try:
                    k = input("What k-value do you want for this graph? ")
                    k = int(k)
                    break
                except:
                    print("Sorry, I couldn't read one of those numbers. Please try again")
    print(f'Saving to {filename}...')
    with open(filename, 'w') as file:
        for ix in range(graph_num):
            nodes = k * (ix+1)
            while nodes%k != 0:
                nodes += 1
            print(nodes)
            if max_edges(nodes) > nodes*k:
                edges = random.randint(nodes*k,max_edges(nodes))
            else:
                edges = random.randint(0,max_edges(nodes))
            for _ in range(GRAPHS_PER_SIZE):
                save_to_open_file(generate_graph(nodes, edges), file, ix, k)    
        
def gen_range(low, high):
    '''runs auto_graph_gen on all k-values from low to high'''
    for k in range(low, high+1):
        filename = f'testing_graphs/data_{k}_partite.csv'
        auto_graph_gen(filename, 150, k)

def max_edges(n):
    '''Generates triangle numbers (used for auto_graph_gen)
    Triangle numbers formula: T_n = T_(n-1) + n
    T_0 = 0
    >>> triangle_nums(3)
    >>> 6'''
    return (n*(n-1))/2

def main():
    while True:
        try:
            low = input('lowest k-value? ')
            high = input('highest k-value? ')
            low = int(low)
            high = int(high)
            break
        except KeyError:
            print("Sorry, please try again")
    gen_range(low, high)
    return
    '''
    while True:
        try:
            graph_num = input("How many graphs do you want? ")
            graph_num = int(graph_num)
            break
        except:
            print("Sorry, please try again")
    gen_method = input("Type 'self' if you want to control the parameters youself, otherwise they will be done automatically. ")
    if gen_method.lower() in ['self', 's', 'myself']:
        manual_graph_gen(filename, graph_num)
    else:
        auto_graph_gen(filename, graph_num)
        '''
        
if __name__ == '__main__':
    main()