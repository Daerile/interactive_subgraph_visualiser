import networkx as nx
import pandas as pd
from collections import deque
from src.backend.node import Node


class GraphSystem:
    def __init__(self, dataframe: pd.DataFrame, column_names, must_have_pairings, optional_pairings):
        self.dataframe = dataframe
        self.nodes = None
        self.digraph = None
        self.column_names = column_names
        self.must_have_columns = ['node_id', 'sub_id', 'connections']
        self.optional_columns = ['node_name', 'sub_id_value_name']
        self.must_have_pairings = must_have_pairings
        self.optional_pairings = optional_pairings
        self.create_nodes()
        self.create_graph()

    def create_nodes(self):
        nodes = []
        for index, next_node in self.dataframe.iterrows():
            if next_node[self.must_have_pairings['node_id']] == '':
                continue
            is_already_in = False
            for node in nodes:
                if node.id == next_node[self.must_have_pairings['node_id']]:
                    node.append_diff_sub_id(next_node)
                    is_already_in = True
                    break
            if not is_already_in:
                nodes.append(Node(next_node, self.column_names, self.must_have_pairings, self.optional_pairings))
        self.nodes = nodes

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
        self.digraph = digraph

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

