import pygame as pg

from src.view.view import View
import unittest
from unittest.mock import patch, mock_open, MagicMock


class TestView(unittest.TestCase):
    @patch('src.view.view.pgui')
    @patch('src.view.view.UIPanel')
    @patch('src.view.view.UIGraph')
    @patch('src.view.view.UIHeader')
    @patch('src.view.view.json')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.view.view.ViewModel')
    @patch('src.view.view.pg')
    def test_init_no_focused(self, mock_pg, mock_view_model, mock_open, mock_json, mock_ui_header, mock_ui_graph, mock_ui_panel, mock_pgui):
        digraph = MagicMock()
        view = View(digraph)

        self.assertEqual(view.digraph, digraph)
        self.assertIsNone(view.focused_graph)
        self.assertEqual(view.focused, False)
        self.assertEqual(view.WIDTH, 1280)
        self.assertEqual(view.HEIGHT, 720)
        self.assertEqual(view.HEADER_WIDTH, 1280)
        self.assertEqual(view.HEADER_HEIGHT, 35)
        self.assertEqual(view.PANEL_WIDTH, 380)
        self.assertEqual(view.PANEL_HEIGHT, 720 - 35 + 5)
        self.assertEqual(view.GRAPH_WIDTH, 1280 - 380 + 5)
        self.assertEqual(view.GRAPH_HEIGHT, 720 - 35 + 5)
        self.assertEqual(view.NODE_RADIUS, 15)

        mock_pg.init.assert_called_once()
        mock_view_model.assert_called_once()
        mock_pg.display.set_mode.assert_called_once()