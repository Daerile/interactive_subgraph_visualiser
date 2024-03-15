import os
import unittest
import pandas as pd
import networkx as nx
from src.backend.graph_system import GraphSystem


class GraphSystemTest(unittest.TestCase):
    def test_create_graph(self):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(script_dir, 'files_for_testing/basic_graph.csv')
        dataframe = pd.read_csv(filepath, sep=';')
        gs = GraphSystem(dataframe)
        self.assertEqual(len(gs.digraph.nodes), 5)
        self.assertEqual(len(gs.digraph.edges), 6)
