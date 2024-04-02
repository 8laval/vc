""""

MVC SOLVER using Branch and Bound algorithm 

"""

from graph import Graph
from heuristic import Heuristic


class MVC:


    @staticmethod
    def bnr(graph: Graph):
        """
        Returns size of MVC using branch and reduce algorithm implementation
        """

        best = MVC.approx(graph)

        def rec(g: Graph, s: set):
            nonlocal best
            g, s = MVC.reduce(g, s, best)

            # Checks for stopping condition
            if len(s) > best or g.e > (best - len(s) - 1) ** 2:
                pass  # No MVC can be found on this branch
            # Checks if it has already arrived at a vertex cover 
            elif g.e == 0:
                best = min(best, len(s))  # Updates the best solution accordingly
            # Else, if no vertex cover is found, branch 
            else:
                # Select vertex of highest degree
                v_max = Heuristic.highest_degree(g)
                # Right branch removes v_max from the graph and adds it to the solution
                rec(g.remove(v_max), s.add(v_max))
                # Left removes all the neighbors of v_max from the graph and adds them to the solution
                nbs = g.neighbors(v_max)
                rec(g.remove(nbs), s.add(nbs))

        rec(graph, set())
        return best

    @staticmethod
    def reduce(g: Graph, s: set, best: int):
        """
        Returns graph G' and solution set s' after application of reduction rules
        """
        graph_changed = True
        if s:
            s = s.copy()
        else:
            s = set()
        # Apply repeatedly until the graph stops changing
        while graph_changed:
            graph_changed = False

            # Degree-one reduction rule
            degree_one_vertices = g.degree_n_vertices(1)
            while bool(degree_one_vertices):
                v = degree_one_vertices.pop()
                nb = g.neighbors(v)[0]
                g = g.remove(nb)
                s.add(nb)
                degree_one_vertices = g.degree_n_vertices(1)
                graph_changed = True

            # Degree-two-triangle reduction rule
            degree_two_vertices = g.degree_n_vertices(2)
            while bool(degree_two_vertices):
                v = degree_two_vertices.pop()
                nbs = g.neighbors(v)
                g = g.remove(nbs)
                s.update(nbs)
                degree_two_vertices = g.degree_n_vertices(2)
                graph_changed = True

            # High degree reduction rule
            high_degree_vertices = g.degree_at_least_n_vertices(best)
            while bool(high_degree_vertices):
                v = high_degree_vertices.pop()
                g = g.remove(v)
                s.add(v)
                high_degree_vertices = g.degree_at_least_n_vertices(best)
                graph_changed = True
        return g, s

    @staticmethod
    def approx(g: Graph):
        """
        Returns approximate of the best solution using a greedy algorithm
        """
        solution = set()
        # Apply reduction rules to the graph
        best = g.e
        g, reduced_solution = MVC.reduce(g, solution, best)
        solution.update(reduced_solution)
        # Remove the largest degree vertex and repeat until a solution is found
        while g.e > 0:
            # Select vertex of highest degree
            v_max = g.highest_degree()[0]
            g = g.remove(v_max)
            solution.add(v_max)

        return len(solution)