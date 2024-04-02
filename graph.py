"""

Graph representation 

"""

import copy
from networkx import barabasi_albert_graph, Graph


def generate_ba_graph(n, m):
    """
    Generates a random graph using the Barabási-Albert preferential attachment model.

    Parameters:
        n (int): Number of nodes in the graph.
        m (int): Number of edges to attach from a new node to existing nodes.

    Returns:
        Graph: A random graph generated using the NetworkX Barabási-Albert model.
    """

    custom_graph = Graph()
    #seed = randint(0, 2 ** 32 - 1)
    nx_graph = barabasi_albert_graph(n, m)
    custom_graph.v = nx_graph.number_of_nodes()
    custom_graph.e = nx_graph.number_of_edges()
    custom_graph.adj = {}

    for node in nx_graph.nodes():
        custom_graph.adj[node] = list(nx_graph.neighbors(node))

    return custom_graph


class Graph:
    """
    Represents an undirected graph using adjacency list 

    Attributes: 
        path: Path to the graph's datapoint
        adj: Adjacency matrix stored as a dictionary
        e: Number of edges
        v: Number of vertices
    """

    def __init__(self, path=None, adj={}, e=0, v=0):
        """
        Constructor for the Graph class 
        """
        if path is not None:
            self.adj = {}
            self.path = path

            with open(path, 'r') as file:
                lines = file.readlines()

            self.v, self.e = map(lambda s: int(''.join(filter(str.isdigit, s))), lines[0].strip().split())

            for i, line in enumerate(lines[1:]):
                self.adj[i + 1] = list(map(int, line.strip().split()))
        else:
            self.adj = adj
            self.v = v
            self.e = e

    def degree(self, node):
        """
        Return the degree of the node
        """
        return len(self.adj[node])

    def neighbors(self, node):
        """
        Return the neighbor list of the node
        """
        return self.adj[node]

    def remove(self, nodes):
        """
        Return new graph with the removed nodes
        """

        if isinstance(nodes, int):
            # Convert single node to a list
            nodes = [nodes]

        new_adj = copy.deepcopy(self.adj)
        new_v = self.v - len(nodes)
        new_e = self.e

        for n in nodes:
            neighbors = new_adj[n]
            del new_adj[n]

            for nb in neighbors:
                new_e -= 1
                new_adj[nb].remove(n)
                # If no more edges, remove node in
        return Graph(adj=new_adj, e=new_e, v=new_v)

    def highest_degree(self):
        """
        Return vertex of the highest degree in the graph instance
        """
        max_degree = -1
        max_vertex = None

        for vertex, neighbors in self.adj.items():
            degree = len(neighbors)
            if degree > max_degree:
                max_degree = degree
                max_vertex = vertex

        return max_vertex, max_degree

    def degree_n_vertices(self, n: int):
        """
        Return set of all vertices of degree n
        """
        vs = set()
        vertices = list(self.adj.keys())
        for v in vertices:
            if self.degree(v) == n:
                vs.add(v)
        return vs

    def degree_at_least_n_vertices(self, n: int):
        """
        Return set of all vertices of degree at least n
        """
        vs = set()
        vertices = list(self.adj.keys())
        for v in vertices:
            if self.degree(v) > n:
                vs.add(v)
        return vs
