import unittest
import pandas as pd
import networkx as nx
from src.backend.graph_system import GraphSystem


class GraphSystemTest(unittest.TestCase):
    def test_create_nodes(self):
        dataframe = pd.read_csv('files_for_testing/basic_graph.csv', sep=';')
        gs = GraphSystem(dataframe)
        self.assertEqual(len(gs.digraph.nodes), 5)
        self.assertEqual(len(gs.digraph.edges), 6)