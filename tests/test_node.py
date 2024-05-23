import math
import unittest

import pandas as pd
import networkx as nx
from src.backend.node import Node


class NodeTest(unittest.TestCase):
    def test_init_node(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
        })

        column_names = ['node_id', 'sub_id', 'connections']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        self.assertEqual(node.id, 'm1')
        self.assertEqual(node.sub_ids, ['0'])
        self.assertEqual(node.sub_id, '0')
        self.assertEqual(node.name, None)
        self.assertEqual(node.names, {})
        self.assertEqual(node.sub_id_value_name, None)
        self.assertEqual(node.sub_id_value_names, {})
        self.assertEqual(node.must_have_pairings, must_have_pairings)
        self.assertEqual(node.optional_pairings, optional_pairings)
        self.assertEqual(node.connections, {'0': ['m2', 'm3']})
        self.assertEqual(node.attributes, {
            'connections': {'0': ['m2', 'm3']}
        })

    def test_init_node_with_name(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
            'node_name': 'node_name'
        })

        column_names = ['node_id', 'sub_id', 'connections', 'node_name']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'node_name',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        self.assertEqual(node.id, 'm1')
        self.assertEqual(node.sub_ids, ['0'])
        self.assertEqual(node.sub_id, '0')
        self.assertEqual(node.name, 'node_name')
        self.assertEqual(node.names, {'0': 'node_name'})
        self.assertEqual(node.sub_id_value_name, None)
        self.assertEqual(node.sub_id_value_names, {})
        self.assertEqual(node.must_have_pairings, must_have_pairings)
        self.assertEqual(node.optional_pairings, optional_pairings)
        self.assertEqual(node.connections, {'0': ['m2', 'm3']})
        self.assertEqual(node.attributes, {
            'connections': {'0': ['m2', 'm3']},
        })

    def test_init_node_with_sub_id_value_name(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
            'sub_id_value_name': 'sub_id_value_name'
        })

        column_names = ['node_id', 'sub_id', 'connections', 'sub_id_value_name']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'sub_id_value_name'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        self.assertEqual(node.id, 'm1')
        self.assertEqual(node.sub_ids, ['0'])
        self.assertEqual(node.sub_id, '0')
        self.assertEqual(node.name, None)
        self.assertEqual(node.names, {})
        self.assertEqual(node.sub_id_value_name, 'sub_id_value_name')
        self.assertEqual(node.sub_id_value_names, {'0': 'sub_id_value_name'})
        self.assertEqual(node.must_have_pairings, must_have_pairings)
        self.assertEqual(node.optional_pairings, optional_pairings)
        self.assertEqual(node.connections, {'0': ['m2', 'm3']})
        self.assertEqual(node.attributes, {
            'connections': {'0': ['m2', 'm3']},
        })

    def test_init_node_with_name_and_sub_id_value_name(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
            'node_name': 'node_name',
            'sub_id_value_name': 'sub_id_value_name'
        })

        column_names = ['node_id', 'sub_id', 'connections', 'node_name', 'sub_id_value_name']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'node_name',
            'sub_id_value_name': 'sub_id_value_name'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        self.assertEqual(node.id, 'm1')
        self.assertEqual(node.sub_ids, ['0'])
        self.assertEqual(node.sub_id, '0')
        self.assertEqual(node.name, 'node_name')
        self.assertEqual(node.names, {'0': 'node_name'})
        self.assertEqual(node.sub_id_value_name, 'sub_id_value_name')
        self.assertEqual(node.sub_id_value_names, {'0': 'sub_id_value_name'})
        self.assertEqual(node.must_have_pairings, must_have_pairings)
        self.assertEqual(node.optional_pairings, optional_pairings)
        self.assertEqual(node.connections, {'0': ['m2', 'm3']})
        self.assertEqual(node.attributes, {
            'connections': {'0': ['m2', 'm3']},
        })

    def test_init_node_with_attributes(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
            'mertekegyseg': 'kg',
            'mennyiseg': 1
        })

        column_names = ['node_id', 'sub_id', 'connections', 'mertekegyseg', 'mennyiseg']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        self.assertEqual(node.id, 'm1')
        self.assertEqual(node.sub_ids, ['0'])
        self.assertEqual(node.sub_id, '0')
        self.assertEqual(node.name, None)
        self.assertEqual(node.names, {})
        self.assertEqual(node.sub_id_value_name, None)
        self.assertEqual(node.sub_id_value_names, {})
        self.assertEqual(node.must_have_pairings, must_have_pairings)
        self.assertEqual(node.optional_pairings, optional_pairings)
        self.assertEqual(node.connections, {'0': ['m2', 'm3']})
        self.assertEqual(node.attributes, {
            'connections': {'0': ['m2', 'm3']},
            'mertekegyseg': 'kg',
            'mennyiseg': 1
        })

    def test_init_node_with_nan_connections(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': math.nan,
        })

        column_names = ['node_id', 'sub_id', 'connections']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        self.assertEqual(node.id, 'm1')
        self.assertEqual(node.sub_ids, ['0'])
        self.assertEqual(node.sub_id, '0')
        self.assertEqual(node.name, None)
        self.assertEqual(node.names, {})
        self.assertEqual(node.sub_id_value_name, None)
        self.assertEqual(node.sub_id_value_names, {})
        self.assertEqual(node.must_have_pairings, must_have_pairings)
        self.assertEqual(node.optional_pairings, optional_pairings)
        self.assertEqual(node.connections, None)
        self.assertEqual(node.attributes, {
            'connections': None
        })

    def test_add_connections(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
        })

        column_names = ['node_id', 'sub_id', 'connections']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        self.assertEqual(node.connections, {'0': ['m2', 'm3']})

        pd_series_2 = pd.Series({
            'node_id': 'm1',
            'sub_id': '-1',
            'connections': 'm2,m4,',
        })

        node.add_connections(pd_series_2)

        self.assertEqual(
            node.connections,
            {'0': ['m2', 'm3'], '-1': ['m2', 'm4']}
        )

    def test_append_diff_sub_id(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
        })

        column_names = ['node_id', 'sub_id', 'connections']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        pd_series_2 = pd.Series({
            'node_id': 'm1',
            'sub_id': '-1',
            'connections': 'm2,m4,',
        })

        node.append_diff_sub_id(pd_series_2)

        self.assertEqual(
            node.connections,
            {'0': ['m2', 'm3'], '-1': ['m2', 'm4']}
        )

        self.assertEqual(
            node.attributes,
            {'connections': {'0': ['m2', 'm3'], '-1': ['m2', 'm4']}}
        )

    def test_append_diff_sub_id_with_names(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
            'node_name': 'node_name'
        })

        column_names = ['node_id', 'sub_id', 'connections', 'node_name']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'node_name',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        pd_series_2 = pd.Series({
            'node_id': 'm1',
            'sub_id': '-1',
            'connections': 'm2,m4,',
            'node_name': 'node_name_2'
        })

        node.append_diff_sub_id(pd_series_2)

        self.assertEqual(
            node.connections,
            {'0': ['m2', 'm3'], '-1': ['m2', 'm4']}
        )

        self.assertEqual(
            node.attributes,
            {'connections': {'0': ['m2', 'm3'], '-1': ['m2', 'm4']}}
        )

        self.assertEqual(
            node.names,
            {'0': 'node_name', '-1': 'node_name_2'}
        )

    def test_append_diff_sub_id_with_sub_id_value_names(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
            'sub_id_value_name': 'sub_id_value_name'
        })

        column_names = ['node_id', 'sub_id', 'connections', 'sub_id_value_name']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'sub_id_value_name'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        pd_series_2 = pd.Series({
            'node_id': 'm1',
            'sub_id': '-1',
            'connections': 'm2,m4,',
            'sub_id_value_name': 'sub_id_value_name_2'
        })

        node.append_diff_sub_id(pd_series_2)

        self.assertEqual(
            node.connections,
            {'0': ['m2', 'm3'], '-1': ['m2', 'm4']}
        )

        self.assertEqual(
            node.attributes,
            {'connections': {'0': ['m2', 'm3'], '-1': ['m2', 'm4']}}
        )

        self.assertEqual(
            node.sub_id_value_names,
            {'0': 'sub_id_value_name', '-1': 'sub_id_value_name_2'}
        )

    def test_append_diff_sub_id_with_names_and_sub_id_value_names(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
            'node_name': 'node_name',
            'sub_id_value_name': 'sub_id_value_name'
        })

        column_names = ['node_id', 'sub_id', 'connections', 'node_name', 'sub_id_value_name']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'node_name',
            'sub_id_value_name': 'sub_id_value_name'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        pd_series_2 = pd.Series({
            'node_id': 'm1',
            'sub_id': '-1',
            'connections': 'm2,m4,',
            'node_name': 'node_name_2',
            'sub_id_value_name': 'sub_id_value_name_2'
        })

        node.append_diff_sub_id(pd_series_2)

        self.assertEqual(
            node.connections,
            {'0': ['m2', 'm3'], '-1': ['m2', 'm4']}
        )

        self.assertEqual(
            node.attributes,
            {'connections': {'0': ['m2', 'm3'], '-1': ['m2', 'm4']}}
        )

        self.assertEqual(
            node.names,
            {'0': 'node_name', '-1': 'node_name_2'}
        )

        self.assertEqual(
            node.sub_id_value_names,
            {'0': 'sub_id_value_name', '-1': 'sub_id_value_name_2'}
        )

    def test_create_focused_connections(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
        })

        column_names = ['node_id', 'sub_id', 'connections']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        pd_series_2 = pd.Series({
            'node_id': 'm1',
            'sub_id': '-1',
            'connections': 'm2,m4,',
        })

        node.append_diff_sub_id(pd_series_2)

        node_2_pd_series = pd.Series({
            'node_id': 'm2',
            'sub_id': '0',
            'connections': 'm3,',
        })

        node_4_pd_series = pd.Series({
            'node_id': 'm4',
            'sub_id': '-1',
            'connections': '',
        })

        node_2 = Node(node_2_pd_series, column_names, must_have_pairings, optional_pairings)
        node_4 = Node(node_4_pd_series, column_names, must_have_pairings, optional_pairings)

        edges = [(node, node_2), (node, node_4)]

        node.create_focused_connections(edges)

        self.assertEqual(
            node.focused_connections,
            {
                '0': ['m2'],
                '-1': ['m2', 'm4']
            }
        )

    def test_create_focused_connections_with_no_connections(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': '',
        })

        column_names = ['node_id', 'sub_id', 'connections']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        pd_series_2 = pd.Series({
            'node_id': 'm1',
            'sub_id': '-1',
            'connections': '',
        })

        node.append_diff_sub_id(pd_series_2)

        node_2_pd_series = pd.Series({
            'node_id': 'm2',
            'sub_id': '0',
            'connections': '',
        })

        node_4_pd_series = pd.Series({
            'node_id': 'm4',
            'sub_id': '-1',
            'connections': '',
        })

        node_2 = Node(node_2_pd_series, column_names, must_have_pairings, optional_pairings)
        node_4 = Node(node_4_pd_series, column_names, must_have_pairings, optional_pairings)

        edges = [(node, node_2), (node, node_4)]

        node.create_focused_connections(edges)

        self.assertEqual(
            node.focused_connections,
            {
                '0': [],
                '-1': []
            }
        )

    def test_create_focused_connections_with_no_edges(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
        })

        column_names = ['node_id', 'sub_id', 'connections']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        pd_series_2 = pd.Series({
            'node_id': 'm1',
            'sub_id': '-1',
            'connections': 'm2,m4,',
        })

        node.append_diff_sub_id(pd_series_2)

        edges = []

        node.create_focused_connections(edges)

        self.assertEqual(
            node.focused_connections,
            {
                '0': [],
                '-1': []
            }
        )

    def test_create_focused_connections_with_no_edges_and_no_connections(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': '',
        })

        column_names = ['node_id', 'sub_id', 'connections']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        pd_series_2 = pd.Series({
            'node_id': 'm1',
            'sub_id': '-1',
            'connections': '',
        })

        node.append_diff_sub_id(pd_series_2)

        edges = []

        node.create_focused_connections(edges)

        self.assertEqual(
            node.focused_connections,
            {
                '0': [],
                '-1': []
            }
        )

    def test_get_connections(self):
        pd_series = pd.Series({
            'node_id': 'm1',
            'sub_id': '0',
            'connections': 'm2,m3,',
        })

        column_names = ['node_id', 'sub_id', 'connections']
        must_have_pairings = {
            'node_id': 'node_id',
            'sub_id': 'sub_id',
            'connections': 'connections'
        }
        optional_pairings = {
            'node_name': 'None',
            'sub_id_value_name': 'None'
        }

        node = Node(pd_series, column_names, must_have_pairings, optional_pairings)

        self.assertEqual(node.get_connected_nodes(), {'m2', 'm3'})

if __name__ == "__main__":
    unittest.main()
