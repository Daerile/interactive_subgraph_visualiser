import os
import unittest
import pandas as pd
import networkx as nx
from src.backend.graph_system import GraphSystem


def load_dataframe(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, f'files_for_testing/test_graph_system/{file_name}')
    return pd.read_csv(filepath, sep=';', encoding='cp1250')

class GraphSystemTest(unittest.TestCase):
    def test_create_graph_from_empty(self):
        dataframe = pd.DataFrame()

        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }
        gs = GraphSystem(dataframe, dataframe.columns, must_have_pairings, optional_pairings)
        self.assertEqual(len(gs.digraph.nodes), 0)
        self.assertEqual(len(gs.digraph.edges), 0)
    def test_create_basic_graph(self):
        dataframe = load_dataframe('basic_graph.csv')

        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }
        gs = GraphSystem(dataframe, dataframe.columns, must_have_pairings, optional_pairings)
        self.assertEqual(len(gs.digraph.nodes), 5)
        self.assertEqual(len(gs.digraph.edges), 6)

    def test_create_graph_with_optional_columns(self):
        dataframe = load_dataframe('graph_with_optionals.csv')

        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'node_name',
            'sub_id_value_name': 'sub_id_value_name'
        }
        gs = GraphSystem(dataframe, dataframe.columns, must_have_pairings, optional_pairings)

        node_names = ["alma", "korte", "szilva", "barack", "cseresznye"]
        sub_id_value_names = ["piros", "zold", "kek", "sarga", "barna"]
        for i, node in enumerate(gs.nodes):
            self.assertEqual(node_names[i], node.name)
            self.assertEqual(sub_id_value_names[i], node.sub_id_value_name)

        self.assertEqual(len(gs.digraph.nodes), 5)
        self.assertEqual(len(gs.digraph.edges), 6)

    def test_create_graph_with_optional_columns_and_no_node_name(self):
        dataframe = load_dataframe('graph_with_optionals_no_node_name.csv')

        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'sub_id_value_name'
        }
        gs = GraphSystem(dataframe, dataframe.columns, must_have_pairings, optional_pairings)

        sub_id_value_names = ["piros", "zold", "kek", "sarga", "barna"]
        for i, node in enumerate(gs.nodes):
            self.assertEqual(sub_id_value_names[i], node.sub_id_value_name)
            self.assertEqual(None, node.name)

        self.assertEqual(len(gs.digraph.nodes), 5)
        self.assertEqual(len(gs.digraph.edges), 6)

    def test_create_graph_with_optional_columns_and_no_sub_id_value_name(self):
        dataframe = load_dataframe('graph_with_optionals_no_sub_id_value_name.csv')

        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'node_name',
            'sub_id_value_name': 'None'
        }
        gs = GraphSystem(dataframe, dataframe.columns, must_have_pairings, optional_pairings)

        node_names = ["alma", "korte", "szilva", "barack", "cseresznye"]
        for i, node in enumerate(gs.nodes):
            self.assertEqual(node_names[i], node.name)
            self.assertEqual(None, node.sub_id_value_name)

        self.assertEqual(len(gs.digraph.nodes), 5)
        self.assertEqual(len(gs.digraph.edges), 6)

    def test_create_graph_with_not_specified_columns(self):
        dataframe = load_dataframe('graph_with_not_specified_columns.csv')

        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }

        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        remaining_columns = ['mertekegyseg', 'mennyiseg']
        mertek_egyseg = ['kg', 'liter', 'kg', 'kg', 'kg']
        mennyiseg = [1, 3, 1, 4, 2]

        gs = GraphSystem(dataframe, dataframe.columns, must_have_pairings, optional_pairings)
        for i, node in enumerate(gs.nodes):
            self.assertTrue('mertekegyseg' in node.attributes)
            self.assertTrue('mennyiseg' in node.attributes)

            self.assertEqual(mertek_egyseg[i], node.attributes['mertekegyseg'])
            self.assertEqual(mennyiseg[i], node.attributes['mennyiseg'])

        self.assertEqual(len(gs.digraph.nodes), 5)
        self.assertEqual(len(gs.digraph.edges), 6)

    def test_graph_with_sub_ids(self):
        dataframe = load_dataframe('graph_with_sub_ids.csv')

        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }

        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        gs = GraphSystem(dataframe, dataframe.columns, must_have_pairings, optional_pairings)
        for node in gs.nodes:
            node_connections = node.get_connected_nodes()
            print(node.connections)
        self.assertEqual(len(gs.digraph.nodes), 5)
        self.assertEqual(len(gs.digraph.edges), 6)

    def test_graph_with_sub_ids_and_optional_columns(self):
        dataframe = load_dataframe('graph_with_sub_ids_and_optionals.csv')

        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }

        optional_pairings = {
            'node_name': 'node_name',
            'sub_id_value_name': 'sub_id_value_name'
        }

        gs = GraphSystem(dataframe, dataframe.columns, must_have_pairings, optional_pairings)
        for node in gs.nodes:
            node_connections = node.get_connected_nodes()
            print(node.connections)
        self.assertEqual(len(gs.digraph.nodes), 5)
        self.assertEqual(len(gs.digraph.edges), 6)


if __name__ == "__main__":
    unittest.main()
