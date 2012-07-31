#-------------------------------------------------------------------------------
# Name:        graph analysis
#
# Author:      mourad mourafiq
#
# Copyright:   (c) mourad mourafiq 
#-------------------------------------------------------------------------------
#!/usr/bin/env python
from __future__ import division

def link(graph, node1, node2):
    """
    Create a link between node1 and node2
    """
    if node1 not in graph:
        graph[node1] = {}
    graph[node1][node2] = 1 
    if node2 not in graph:
        graph[node2] = {}
    graph[node2][node1] = 1

def add_node(graph_to, graph_from, node):
    if node not in graph_to:
        graph_to[node] = graph_from[node]
        for neighbor in graph_to[node].keys():
            graph_to = add_node(graph_to, graph_from, neighbor)
    return graph_to
        
        
def shortest_path(graph, node1, node2):
    """
    Finds the shortest path from node1 in node 2 in graph.
    """        
    if node1 == node2:
        return [node1]
    explored = []
    to_explore = [[node1]]
    while to_explore:
        path = to_explore.pop(0)
        s = path[-1]
        for successor in graph[s].keys():
            if successor not in explored:
                explored.append(successor)
                path2 = path + [successor]
                if node2 == successor:
                    return path2
                to_explore.append(path2)
    return []
            
def longest_path(graph, node=None):
    """
    Returns the longest path in the graph if node is None
    I f node is not None, then it returns the longest path from node
    """
    if node is not None:
        return max([shortest_path(graph, node, successor) for successor in graph.keys()], key=len)
    return max([shortest_path(graph, a, b) for a in graph.keys() for b in graph.keys()], key=len)

def centrality(graph, node):
    """
    Returns the centrality of node in graph
    """    
    return sum([len(shortest_path(graph, node, successor)) for successor in graph.keys()])/len(graph.keys())

def indep_graphs(graph): 
    """
    Returns the independent graphs in the current graph
    """
    graphs = []     
    def which_graph(node):
        for g in graphs:
            if node in g: return g 
        return {}
        
    for node in graph.keys():
        g = add_node(which_graph(node), graph, node)
        if g not in graphs: graphs.append(g)        
    return graphs

def graph_for_node(graph, node):
    """
    Returns the independent graph containing node
    """
    return  add_node({}, graph, node)    
        
def check_pairwise_connectivity(graph, node1, node2):
    """
    checks the connectivity between two nodes, 
    and returns True if connected, otherwise False    
    """
    return True if node2 in graph_for_node(graph, node1) else False
    
def clustering_coef(graph, node, verbose=False):
    """
    calculates the clustering coef for a particular node in the graph
     let Dn = node degree
         Vn = number of links between neighbors of the node
    """
    neighbors = graph[node].keys()
    Dn = len(neighbors)
    if Dn == 0 : return Dn;    
    Vn = 0
    for neighbor1 in neighbors:
        index1 = neighbors.index(neighbor1)
        for neighbor2 in neighbors:
            index2 = neighbors.index(neighbor2)
            if index1 < index2 and neighbor2 in graph[neighbor1]: Vn += 1
    coef = (2 * Vn) / (Dn * (Dn - 1))
    if verbose: print '%s\'s degree : %s, links between neighbors : %s. Culestering coef : %s' % (node, Dn, Vn, coef)    
    return coef 

def average_cluestering(graph, verbose=True):
    average = sum([clustering_coef(graph, node, verbose=verbose) for node in graph])/len(graph)
    if verbose: print average
    return average

G = {}
connections = [('a', 'g'), ('a', 'd'), ('d', 'g'), ('g', 'c'), ('b', 'f'), ('f', 'e'), ('e', 'h')]
for x,y in connections: link(G, x, y)
g = graph_for_node(G, 'a')
print g
print shortest_path(G, 'a', 'c')
print shortest_path(g, 'a', 'd')
print centrality(g, 'a')
