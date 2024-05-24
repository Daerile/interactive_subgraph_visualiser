import pygame as pg
import pygame_gui as pgui
import numpy as np
import pandas as pd
import networkx as nx
from random import random

from collections import deque

import pprint
import cProfile
import pstats

from src.view.layout import Layout

import unittest
from unittest.mock import patch, mock_open, MagicMock, call, PropertyMock


class TestLayout(unittest.TestCase):
    def setUp(self):
        self.patcher_create_view = patch.object(Layout, 'create_view')
        self.mock_create_view = self.patcher_create_view.start()

    def tearDown(self):
        self.patcher_create_view.stop()

    def test_init(self):
        digraph = nx.DiGraph()

        node_mock = MagicMock()
        node_mock.id = 'something'
        digraph.add_node(node_mock)
        nodes = [node_mock]
        cem = MagicMock()
        layout = Layout(digraph, cem)
        self.assertEqual(layout.WIDTH, 3000)
        self.assertEqual(layout.HEIGHT, 3000)
        self.assertEqual(layout.nodes, nodes)
        self.assertEqual(layout.edge_list, [])
        self.assertEqual(layout.node_map, {'something': 0})
        self.assertEqual(layout.adjacency_list, [[]])
        self.assertEqual(layout.complement_adjacency_list, [[]])
        self.assertEqual(layout.cem, cem)

        self.mock_create_view.assert_called_once_with(digraph)

    def test_create_view_focused(self):
        digraph = nx.DiGraph()
        node_mock = MagicMock()
        node_mock.id = 'something'
        digraph.add_node(node_mock)
        cem = MagicMock()
        cem.focused = True
        layout = Layout(digraph, cem)
        self.patcher_create_view.stop()
        with patch.object(layout, 'create_focused_elems') as mock_create_focused_elems:
            layout.create_view(digraph)
            mock_create_focused_elems.assert_called_once_with(digraph)

    def test_create_view_not_focused(self):
        digraph = nx.DiGraph()
        node_mock = MagicMock()
        node_mock.id = 'something'
        digraph.add_node(node_mock)
        cem = MagicMock()
        cem.focused = False
        layout = Layout(digraph, cem)
        self.patcher_create_view.stop()
        with patch.object(layout, 'create_full_elems') as mock_create_full_elems:
            layout.create_view(digraph)
            mock_create_full_elems.assert_called_once()

    def test_create_focused_elems(self):
        digraph = nx.DiGraph()
        node_mock = MagicMock()
        node_mock.id = 'something'
        digraph.add_node(node_mock)
        cem = MagicMock()
        cem.focused = True
        cem.focused_node.id = 'something'
        layout = Layout(digraph, cem)
        with patch.object(layout, 'create_from_layer') as mock_create_from_layer:
            layout.create_focused_elems(digraph)
            self.assertEqual(mock_create_from_layer.call_count, 2)
        cem.create_node_button.assert_called_once()
        cem.create_edges.assert_called_once()
        cem.center_around.assert_called_once()

    def test_create_from_layer(self):
        digraph = nx.DiGraph()
        node_mock = MagicMock()
        node_mock.id = 'something'
        digraph.add_node(node_mock)
        cem = MagicMock()
        cem.focused = True
        cem.focused_node.id = 'something'
        layout = Layout(digraph, cem)
        center_pos = (0, 0)
        x_breakpoints_forwards = [1, 2]
        x_breakpoints_backwards = [1, 2]
        with patch.object(layout, 'create_buttons') as mock_create_buttons:
            layout.create_from_layer(0, center_pos, x_breakpoints_forwards, x_breakpoints_forwards, forward=True)
            self.assertEqual(mock_create_buttons.call_count, 1)

    def test_create_buttons(self):
        digraph = nx.DiGraph()
        node_mock = MagicMock()
        node_mock.id = 'something'
        digraph.add_node(node_mock)
        cem = MagicMock()
        cem.focused = True
        cem.focused_node.id = 'something'
        layout = Layout(digraph, cem)
        layout.nodes = {1: node_mock, 2: node_mock}
        center_pos = (0, 0)
        x_breakpoints_forwards = [1, 2]
        x_breakpoints_backwards = [1, 2]
        next_layer = [1, 2]
        layout.adjacency_list = {1: [1, 2], 2: [1, 2]}
        layout.complement_adjacency_list = {1: [0], 2: [0]}
        y_breakpoints_before = layout.create_buttons(0, 1, 0, 1, next_layer)
        self.assertEqual(cem.create_node_button.call_count, 2)

    def test_create_full_elems(self):
        digraph = nx.DiGraph()
        node_mock = MagicMock()
        node_mock.id = 'something'
        digraph.add_node(node_mock)
        cem = MagicMock()
        cem.focused = False
        layout = Layout(digraph, cem)
        with patch.object(layout, 'init_positions') as mock_init_positions, \
             patch.object(layout, 'fruchterman_reingold') as mock_fruchterman_reingold:
            layout.create_full_elems()
            mock_init_positions.assert_called_once()
            mock_fruchterman_reingold.assert_called_once()
        cem.create_edges.assert_called_once()

    def test_init_positions(self):
        digraph = nx.DiGraph()
        node_mock = MagicMock()
        node_mock.id = 'something'
        digraph.add_node(node_mock)
        cem = MagicMock()
        cem.focused = False
        layout = Layout(digraph, cem)
        layout.init_positions(2000, 2000)
        cem.create_node_button.assert_called_once()


if __name__ == '__main__':
    unittest.main()