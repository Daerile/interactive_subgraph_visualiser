import networkx as nx
import pandas as pd
from collections import deque
from src.backend.node import Node


class GraphSystem:
    def __init__(self, dataframe: pd.DataFrame):
        self.dataframe = dataframe
        self.nodes = self.create_nodes()
        self.digraph = self.create_graph()

    def create_nodes(self):
        nodes = []
        for index, next_node in self.dataframe.iterrows():
            if next_node['csúcsid'] == '':
                continue
            is_already_in = False
            for node in nodes:
                if node.id == next_node['csúcsid']:
                    node.append_diff_subid(next_node)
                    is_already_in = True
                    break
            if not is_already_in:
                nodes.append(Node(next_node))
        return nodes

    def create_graph(self):
        digraph = nx.DiGraph()
        for node in self.nodes:
            digraph.add_node(node)
        for node in self.nodes:
            if node.get_connected_nodes():
                for connected_node in node.get_connected_nodes():
                    if connected_node == node.id:
                        continue
                    for node_in_graph in digraph.nodes:
                        if node_in_graph.id == connected_node:
                            digraph.add_edge(node, node_in_graph)
                            break
        return digraph

    def get_subgraph(self, node_id, depth):
        starter_node = None
        for node in self.digraph.nodes:
            if node.id == node_id:
                starter_node = node

        shortest_path_lengths = nx.single_source_shortest_path_length(self.digraph, starter_node)
        reachable_nodes = {node for node, distance in shortest_path_lengths.items() if distance <= depth}
        return self.digraph.subgraph(reachable_nodes).copy()
