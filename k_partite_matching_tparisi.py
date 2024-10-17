#!/usr/bin/python3
import generate_graphs_tparisi as gen
import sys
import argparse
import time
import networkx as nx
import graph_results_tparisi as plot
import re
import os

'''NOTE:
This program makes the assumption that the nodes it is given are already assigned to their groups based on placement.
It divides the nodes into k groups based on positioning. For example, if there are 9 nodes and k=3, it assumes nodes
1-3 are in group 1, 4-6 are in group 2, and 7-9 are in group 3.'''

### GLOBALS
CORRECT = False

### FUNCTIONS
def still_solvable(graph: nx.Graph, k: int, used_node_count):
    '''Checks to see if there are any nodes that cannot possibly reach k connections with the current choices'''
    if graph.number_of_nodes() == 0:
        return True
    for node in graph.nodes():
        if not list(graph.neighbors(node)) and node not in used_node_count.keys():
            return False
    return True

def solve(graph: nx.Graph, k: int, verbose=False):
    '''Solve: Returns whether or not a k-partite matching exists for the given dataset'''
    '''Pseudocode:
    groups = split graph into k groups
    for neighboring groups (grp1, grp2) in groups:
        if no bipartite match between grp1 and grp2:
            return False
    return True
    '''
    # Split graph into k_groups, label each node with its group #
    group_size = len(graph.nodes())//k
    labels = {}
    for node in graph.nodes():
        node_no = int(node)
        group_no = node_no // group_size
        labels[node] = group_no
    nx.set_node_attributes(graph, labels, 'group')
    if k == 2:
        # If k is 2 just run a bipartite comparison
        g1_list = []
        g2_list = []
        for node in graph.nodes():
            if graph.nodes[node]['group'] == 0:
                g1_list.append(node)
            elif graph.nodes[node]['group'] == 1:
                g2_list.append(node)
        if not bipartite_setup_and_check(graph, g1_list, g2_list, verbose):
            return False
    else:
        # If k > 2 check all groups
        for group1 in range(k):
            for group2 in range(group1+1, k):
                g1_list = []
                g2_list = []
                for node in graph.nodes():
                    if graph.nodes[node]['group'] == group1:
                        g1_list.append(node)
                    elif graph.nodes[node]['group'] == group2:
                        g2_list.append(node)
                if not bipartite_setup_and_check(graph, g1_list, g2_list, verbose):
                    return False
    return True
    
def bipartite_setup_and_check(graph, g1, g2, verbose=False):
    ''' Extracts relevant edges when checking for bipartite matching between the two groups '''
    relevant_edges = []
    edge_count = {}
    for node in g1:
        for neighbor in nx.all_neighbors(graph, node):
            if neighbor in g2:
                relevant_edges.append((node, neighbor))
                edge_count[node] = edge_count.get(node, 0) + 1
                edge_count[neighbor] = edge_count.get(neighbor, 0) + 1
    # Check for bipartite matching
    return bipartite_check(g1, g2, relevant_edges, edge_count, verbose)

def bipartite_check(g1, g2, edges, counts, verbose=False):
    '''Checks two groups of nodes and sees if they can form a perfect bipartite match'''
    # Finish conditions
    if len(g1) != len(g2):
        #print("Check how you remove nodes from g1 and g2")
        return False
    if not g1 and not g2:
        return True
    # Look for nodes with only 1 relevant edge
    for key, val in counts.items():
        if val == 1:
            for edge in edges:
                if key in edge:
                    # See if it can be solved with that edge, otherwise must be false
                    #print_data(g1, g2, edges, edge, counts)
                    # New data is data removing anything related to the selected edge
                    [new_g1, new_g2, new_edges, new_counts] = create_new_data(g1, g2, edges, edge, counts, verbose)
                    # Check for defined error code -1
                    if -1 in new_g1:
                        return False
                    if bipartite_check(new_g1, new_g2, new_edges, new_counts, verbose):
                        return True
                    #print("Failure: Single edge did not lead to correct graph")
                    return False
    # If no nodes with 1 relevant edge, try taking each node and see if a solution can be found
    for edge in edges:
        #print_data(g1, g2, edges, edge, counts)
        [new_g1, new_g2, new_edges, new_counts] = create_new_data(g1, g2, edges, edge, counts)
        if -1 in new_g1:
            return False
        if bipartite_check(new_g1, new_g2, new_edges, new_counts, verbose):
            return True
    return False

def print_data(g1, g2, edges, edge, counts):
    print(g1)
    print(g2)
    print(edges)
    print(edge)
    print(counts)

def create_new_data(g1, g2, edges, edge, counts, verbose=False):
    '''Updates g1, g2, edges, and count s.t. edge and its nodes are not included'''
    # Need to:
    # a. Update counts
    # b. Remove edges connected to either node
    # c. Update g1 and g2
    new_edges = []
    new_counts = counts
    new_counts[edge[0]] -= 1
    new_counts[edge[1]] -= 1
    new_g1 = g1
    new_g2 = g2
    try:
        if edge[0] in new_g1:
            new_g1.remove(edge[0])
            new_g2.remove(edge[1])
        else:
            new_g2.remove(edge[0])
            new_g1.remove(edge[1])
    except:
        '''Returns specified error value if the nodes aren't in two different groups. This means the edge would not be part of a k-partite graph'''
        new_g2 = [-1]
        new_g1 = [-1]
    for new_edge in edges:
        if edge[0] not in new_edge and edge[1] not in new_edge:
            new_edges.append(new_edge)
    return new_g1, new_g2, new_edges, new_counts
    
def get_filenames_with_from_os(directory, regex_pattern=None):
    '''Loads all files from the given directory, only matches regex pattern if one is given.'''

    filenames = []

    for filename in os.listdir(directory):
        if regex_pattern:
            if re.search(regex_pattern, filename):
                filenames.append(directory + filename)
        else:
            filenames.append(directory + filename)

    return filenames

def manual_filenames():
    '''Creates list of filenames by prompting the user'''
    print("Please enter the names of the files you want to analyze")
    filenames = []
    while True:
        name = input('Next file (type STOP to quit): ')
        if name.upper() == 'STOP':
            break
        filenames.append(name)
    return filenames

def print_results(result_data):
    '''Text-based output for how long each file took to solve'''
    for result, time in result_data.items():
        print(f'Graph #{result} completed in {time:.10f} seconds')

### MAIN
def main(args=sys.argv[1:]):
    filenames = []
    if args:
        for arg in args:
            if 'testing_graphs/' in arg:
                filenames.append(arg)
    else:
        filenames = manual_filenames()
    X_t = []
    Y_t = []
    X_f = []
    Y_f = []
    for file in filenames:
        print(f'Solving {file}...')
        graphs = gen.load_from_file(file)
        num_graphs = len(graphs)
        for num, G in enumerate(graphs, start=1):
            #print(f'Graph {num} of {num_graphs}')
            start = time.time()
            if num == 127:
                correct = solve(G, G.graph["k"], True)
            else:
                correct = solve(G, G.graph["k"])
            end = time.time()
            if correct:
                Y_t.append(end - start)
                X_t.append(len(G.nodes()))
            else:
                Y_f.append(end - start)
                X_f.append(len(G.nodes()))
            print(f'Graph #{num}/{num_graphs}: {correct}, time={end-start:4f}s')
    plot.graph(X_t, Y_t, X_f, Y_f)
    

if __name__ == '__main__':
    main(sys.argv)
