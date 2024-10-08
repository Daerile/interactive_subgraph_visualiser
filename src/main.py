from src.view.view import View
import networkx as nx


def main():
    nx_graph = nx.empty_graph()
    view = View(nx_graph)
    view.run()


if __name__ == '__main__':
    main()
