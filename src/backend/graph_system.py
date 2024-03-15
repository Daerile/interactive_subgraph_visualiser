import networkx as nx
import pandas as pd
from src.backend.node import Node

class GraphSystem:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        self.nodes = self.create_nodes()
        self.digraph = self.create_graph()


    def create_nodes(self):
        nodes = []
        for index, next_node in self.dataframe.iterrows():
            nodes.append(Node(next_node))
        return nodes

    def create_graph(self):
        digraph = nx.DiGraph()
        for node in self.nodes:
            digraph.add_node(node)
        for node in self.nodes:
            if node.connections:
                for connection in node.connections:
                    if connection == node.id :
                        continue
                    for node_in_graph in digraph.nodes:
                        if node_in_graph.id == connection:
                            digraph.add_edge(node, node_in_graph)
                            break
        return digraph


    def get_subgraph(self, node_id, depth):
        NotImplemented
    def BFS(self, root):
        NotImplemented