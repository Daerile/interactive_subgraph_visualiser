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

        forward_subgraph = nx.bfs_tree(self.digraph, starter_node, depth_limit=depth)
        backward_subgraph = nx.bfs_tree(self.digraph.reverse(), starter_node, depth_limit=depth)
        backward_subgraph = backward_subgraph.reverse()

        full_subgraph = nx.compose(forward_subgraph, backward_subgraph)
        for node in full_subgraph.nodes:
            node.create_focused_connections(full_subgraph.edges)
        return full_subgraph

