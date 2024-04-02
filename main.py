"""

Run MVC solver for different graph instances

"""
from graph import Graph, generate_ba_graph
from solver import MVC


def main():
    g1 = Graph("input/instance1.graph")
    g2 = Graph("input/instance2.graph")
    g3 = generate_ba_graph(4, 3)
    g4 = generate_ba_graph(10, 2)

    print(MVC.bnr(g1))
    print(MVC.bnr(g2))
    print(MVC.bnr(g3))
    print(MVC.bnr(g4))


if __name__ == '__main__':
    main()


