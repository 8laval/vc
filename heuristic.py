"""

Heuristic instances 

"""

from graph import Graph


class Heuristic:
    @staticmethod
    def highest_degree(g: Graph):
        return g.highest_degree()[0]
