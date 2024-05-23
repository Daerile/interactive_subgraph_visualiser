import pygame as pg
import networkx as nx

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
    def test_init_focused(self, mock_pg, mock_view_model, mock_open, mock_json, mock_ui_header, mock_ui_graph, mock_ui_panel, mock_pgui):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.handle_light_mode_pressed.return_value = {}
        mock_ui_panel.return_value = mock_ui_panel_return_val

        focused_graph = nx.DiGraph()
        view = View(digraph, focused_graph, True)

        self.assertEqual(view.digraph, digraph)
        self.assertIs(view.focused_graph, focused_graph)
        self.assertEqual(view.focused, True)
        self.assertEqual(view.WIDTH, 1280)
        self.assertEqual(view.HEIGHT, 720)
        self.assertEqual(view.HEADER_WIDTH, 1280)
        self.assertEqual(view.HEADER_HEIGHT, 35)
        self.assertEqual(view.PANEL_WIDTH, 380)
        self.assertEqual(view.PANEL_HEIGHT, 720 - 35 + 5)
        self.assertEqual(view.GRAPH_WIDTH, 1280 - 380 + 5)
        self.assertEqual(view.GRAPH_HEIGHT, 720 - 35 + 5)
        self.assertEqual(view.NODE_RADIUS, 15)
        self.assertEqual(view.dragging, False)
        self.assertIsNone(view.dragged_button)
        self.assertEqual(view.dragged_button_x, 0)
        self.assertEqual(view.dragged_button_y, 0)
        self.assertIsNone(view.res)
        self.assertEqual(view.offset_x, 0)
        self.assertEqual(view.offset_y, 0)
        self.assertEqual(view.zoom_lvl, 0)
        self.assertEqual(view.zoom_scale, 1.0)

        mock_pg.init.assert_called_once()
        mock_view_model.assert_called_once()
        mock_pg.display.set_mode.assert_called_once()
        mock_json.load.assert_called_once()
        mock_json.dump.assert_called_once()
        mock_pgui.UIManager.assert_called_once()
        mock_ui_panel.assert_called_once_with(
            view.window,
            view.manager,
            view.PANEL_WIDTH,
            view.PANEL_HEIGHT,
            view.digraph,
            2,
            3, 3,
            view.HEADER_HEIGHT
        )
        mock_ui_panel_return_val.handle_light_mode_pressed.assert_called_once()
        mock_ui_header.assert_called_once_with(
            view.window,
            view.manager,
            view.HEADER_WIDTH,
            view.HEADER_HEIGHT,
            view.digraph
        )
        mock_ui_graph.assert_called_once_with(
            view.window,
            view.manager,
            view.GRAPH_WIDTH,
            view.GRAPH_HEIGHT,
            view.NODE_RADIUS,
            view.digraph,
            view.PANEL_WIDTH,
            view.HEADER_HEIGHT,
            view.colors
        )
        mock_pg.display.set_caption.assert_called_once_with("Interactive Subgraph Visualiser")

    @patch('src.view.view.pgui')
    @patch('src.view.view.UIPanel')
    @patch('src.view.view.UIGraph')
    @patch('src.view.view.UIHeader')
    @patch('src.view.view.json')
    @patch('builtins.open', new_callable=mock_open)
    @patch('src.view.view.ViewModel')
    @patch('src.view.view.pg')
    def test_init_no_focused(self, mock_pg, mock_view_model, mock_open, mock_json, mock_ui_header, mock_ui_graph,
                             mock_ui_panel, mock_pgui):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.handle_light_mode_pressed.return_value = {}
        mock_ui_panel.return_value = mock_ui_panel_return_val

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
        self.assertEqual(view.dragging, False)
        self.assertIsNone(view.dragged_button)
        self.assertEqual(view.dragged_button_x, 0)
        self.assertEqual(view.dragged_button_y, 0)
        self.assertIsNone(view.res)
        self.assertEqual(view.offset_x, 0)
        self.assertEqual(view.offset_y, 0)
        self.assertEqual(view.zoom_lvl, 0)
        self.assertEqual(view.zoom_scale, 1.0)

        mock_pg.init.assert_called_once()
        mock_view_model.assert_called_once()
        mock_pg.display.set_mode.assert_called_once()
        mock_json.load.assert_called_once()
        mock_json.dump.assert_called_once()
        mock_pgui.UIManager.assert_called_once()
        mock_ui_panel.assert_called_once_with(
            view.window,
            view.manager,
            view.PANEL_WIDTH,
            view.PANEL_HEIGHT,
            view.digraph,
            2,
            3, 3,
            view.HEADER_HEIGHT
        )
        mock_ui_panel_return_val.handle_light_mode_pressed.assert_called_once()
        mock_ui_header.assert_called_once_with(
            view.window,
            view.manager,
            view.HEADER_WIDTH,
            view.HEADER_HEIGHT,
            view.digraph
        )
        mock_ui_graph.assert_called_once_with(
            view.window,
            view.manager,
            view.GRAPH_WIDTH,
            view.GRAPH_HEIGHT,
            view.NODE_RADIUS,
            view.digraph,
            view.PANEL_WIDTH,
            view.HEADER_HEIGHT,
            view.colors
        )
        mock_pg.display.set_caption.assert_called_once_with("Interactive Subgraph Visualiser"