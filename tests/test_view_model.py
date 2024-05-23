import pygame as pg
import pygame_gui as pgui
import numpy as np
import pandas as pd
import networkx as nx

from random import random
from src.viewmodel.view_model import ViewModel

import unittest
from unittest.mock import patch, mock_open, MagicMock

class TestViewModel(unittest.TestCase):
    def test_init(self):
        view_model = ViewModel()
        self.assertIsNone(view_model.column_names)
        self.assertIsNone(view_model.data)
        self.assertIsNone(view_model.graph_system)

    @patch('src.viewmodel.view_model.GraphSystem')
    def test_create_digraph(self, mock_graph_system):
        view_model = ViewModel()
        view_model.data = pd.DataFrame({'col1': ['val1', 'val2'], 'col2': ['val1', 'val2']})
        view_model.column_names = view_model.data.columns
        must_have_pairings = {'col1': 'col2'}
        optional_pairings = {}
        mock_graph_system.return_value = nx.DiGraph()
        mock_graph_system.return_value.digraph = nx.DiGraph()
        result = view_model.create_digraph(must_have_pairings, optional_pairings)
        self.assertIsInstance(result, nx.DiGraph)
        mock_graph_system.assert_called_once_with(view_model.data, view_model.column_names, must_have_pairings, optional_pairings)

    def test_handle_load_button_pressed(self):
        view_model = ViewModel()
        return_val = pd.DataFrame({'col1': ['val1', 'val2'], 'col2': ['val1', 'val2']})
        with patch('src.viewmodel.view_model.Loader.load_file', return_value=return_val) as mock_load_file:
            result = view_model.handle_load_button_pressed()
            self.assertIs(view_model.data, return_val)
            self.assertIs(view_model.column_names, return_val.columns)

    def test_handle_load_button_pressed_none(self):
        view_model = ViewModel()
        with patch('src.viewmodel.view_model.Loader.load_file', return_value=None) as mock_load_file:
            result = view_model.handle_load_button_pressed()
            self.assertIsNone(result)

    @patch('src.viewmodel.view_model.GraphSystem')
    def test_handle_node_focused(self, mock_graph_system):
        view_model = ViewModel()
        view_model.graph_system = mock_graph_system
        view_model.graph_system.get_subgraph.return_value = nx.DiGraph()
        focused_node = MagicMock()
        focused_node.id = 1
        focused_depth = 2
        result = view_model.handle_node_focused(focused_node, focused_depth)
        self.assertIsInstance(result, nx.DiGraph)
        view_model.graph_system.get_subgraph.assert_called_once_with(focused_node.id, focused_depth)

    def test_handle_node_focused_none(self):
        view_model = ViewModel()
        result = view_model.handle_node_focused(None, 1)
        self.assertIsNone(result)

    @patch('src.viewmodel.view_model.Loader.save_file')
    def test_handle_save_button_pressed(self, mock_save_file):
        view_model = ViewModel()
        view_model.data = pd.DataFrame({'col1': ['val1', 'val2'], 'col2': ['val1', 'val2']})
        view_model.column_names = view_model.data.columns
        view_model.graph_system = MagicMock()
        view_model.graph_system.must_have_columns = ['col1']
        view_model.graph_system.optional_columns = ['col2']
        view_model.graph_system.must_have_pairings = {'col1': 'col2'}
        view_model.graph_system.optional_pairings = {}
        export_digraph = nx.DiGraph()
        export_digraph.nodes = [MagicMock()]
        view_model.handle_save_button_pressed(export_digraph)
        mock_save_file.assert_called_once()


if __name__ == '__main__':
    unittest.main()