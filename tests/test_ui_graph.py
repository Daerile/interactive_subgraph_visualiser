import pygame as pg
import pygame_gui as pgui

from src.view.ui_graph import UIGraph

import unittest
from unittest.mock import patch, MagicMock, call


class TestUiGraph(unittest.TestCase):
    @patch('src.view.ui_graph.CanvasElementManager')
    def test_init(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600

        # Act
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)

        # Assert
        self.assertEqual(ui_graph.window, window)
        self.assertEqual(ui_graph.width, width)
        self.assertEqual(ui_graph.height, height)
        self.assertEqual(ui_graph.node_radius, node_radius)
        self.assertEqual(ui_graph.manager, manager)
        self.assertEqual(ui_graph.digraph, digraph)
        self.assertEqual(ui_graph.panel_width, panel_width)
        self.assertEqual(ui_graph.header_height, header_height)
        self.assertIsNone(ui_graph.focused_cem)
        self.assertEqual(ui_graph.colors, colors)
        self.assertEqual(ui_graph.full_cem, mock_canvas_element_manager.return_value)

        mock_canvas_element_manager.assert_called_once_with(digraph, window, manager, colors, node_radius)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_digraph_loaded(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)

        # Act
        new_digraph = MagicMock()
        ui_graph.digraph_loaded(new_digraph)

        # Assert
        self.assertEqual(ui_graph.digraph, new_digraph)
        self.assertEqual(ui_graph.full_cem, mock_canvas_element_manager.return_value)
        self.assertIsNone(ui_graph.focused_cem)
        mock_canvas_element_manager.assert_has_calls([call(digraph, window, manager, colors, node_radius), call(new_digraph, window, manager, colors, node_radius)])
        ui_graph.full_cem.center_around.assert_called_once_with(0, 0, full_cem=True)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_move_all(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.get_current_cem = MagicMock()

        # Act
        ui_graph.move_all(10, 20)

        # Assert
        ui_graph.get_current_cem.assert_called_once()
        ui_graph.get_current_cem().move_all.assert_called_once_with(10, 20)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_zoom_all(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.get_current_cem = MagicMock()

        # Act
        ui_graph.zoom_all(10, 20, (30, 40))

        # Assert
        ui_graph.get_current_cem.assert_called_once()
        ui_graph.get_current_cem().zoom_all.assert_called_once_with(10, 20, (30, 40))

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_process_events(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)

        # Act
        event = MagicMock()
        ui_graph.process_events(event)

        # Assert
        manager.process_events.assert_called_once_with(event)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_draw_ui_empty_digraph(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = []
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.get_current_cem = MagicMock()

        # Act
        ui_graph.draw_ui()

        # Assert
        ui_graph.get_current_cem.assert_not_called()
        manager.draw_ui.assert_called_once_with(window)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_draw_ui(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = [MagicMock()]
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.get_current_cem = MagicMock()

        # Act
        with patch.object(ui_graph, 'get_current_cem') as mock_get_current_cem:
            ui_graph.draw_ui()
            mock_get_current_cem.assert_has_calls([call(), call().draw_arrows(), call(), call().draw_node_buttons()])

        # Assert
        manager.draw_ui.assert_called_once_with(window)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_handle_node_focused_none_cem(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)

        # Act
        focused_digraph = MagicMock()
        focused_node = MagicMock()
        focused_depth = 10
        vertical_scatter = 20
        horizontal_scatter = 30
        ui_graph.handle_node_focused(focused_digraph, focused_node, focused_depth, vertical_scatter, horizontal_scatter)

        # Assert
        self.assertIsNotNone(ui_graph.focused_cem)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_handle_node_focused(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        focused_digraph = MagicMock()
        focused_node = MagicMock()
        focused_depth = 10
        vertical_scatter = 20
        horizontal_scatter = 30
        ui_graph.handle_node_focused(focused_digraph, focused_node, focused_depth, vertical_scatter, horizontal_scatter)

        # Assert
        self.assertIsNotNone(ui_graph.focused_cem)
        ui_graph.focused_cem.update_focus.assert_called_once()

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_handle_return_button_pressed(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        ui_graph.handle_return_button_pressed()

        # Assert
        self.assertIsNone(ui_graph.focused_cem)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_handle_node_selected(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        selected_node = MagicMock()
        ui_graph.handle_node_selected(selected_node)

        # Assert
        ui_graph.focused_cem.selected_node_changed.assert_called_once_with(selected_node)
        ui_graph.full_cem.selected_node_changed.assert_called_once_with(selected_node)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_change_colors(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        new_colors = MagicMock()
        ui_graph.change_colors(new_colors)

        # Assert
        self.assertEqual(ui_graph.colors, new_colors)
        ui_graph.focused_cem.change_colors.assert_called_once_with(new_colors)
        ui_graph.full_cem.change_colors.assert_called_once_with(new_colors)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_handle_edge_selected(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        selected_edge = MagicMock()
        ui_graph.handle_edge_selected(selected_edge)

        # Assert
        ui_graph.focused_cem.selected_edge_changed.assert_called_once_with(selected_edge)
        ui_graph.full_cem.selected_edge_changed.assert_called_once_with(selected_edge)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_handle_edge_selected_none_focused_cem(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)

        # Act
        selected_edge = MagicMock()
        ui_graph.handle_edge_selected(selected_edge)

        # Assert
        ui_graph.full_cem.selected_edge_changed.assert_called_once_with(selected_edge)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_handle_searched_nodes_changed(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        searched_nodes = MagicMock()
        mode = MagicMock()
        ui_graph.handle_searched_nodes_changed(searched_nodes, mode)

        # Assert
        ui_graph.focused_cem.searched_nodes_changed.assert_called_once_with(searched_nodes, mode)
        ui_graph.full_cem.searched_nodes_changed.assert_called_once_with(searched_nodes, mode)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_get_focused_digraph(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        focused_digraph = ui_graph.get_focused_digraph()

        # Assert
        self.assertEqual(focused_digraph, ui_graph.focused_cem.digraph)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_get_focused_digraph_none_focused_cem(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)

        # Act
        focused_digraph = ui_graph.get_focused_digraph()

        # Assert
        self.assertIsNone(focused_digraph)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_get_node_buttons(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        node_buttons = ui_graph.get_node_buttons()

        # Assert
        self.assertEqual(node_buttons, ui_graph.focused_cem.node_buttons)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_get_arrows(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        arrows = ui_graph.get_arrows()

        # Assert
        self.assertEqual(arrows, ui_graph.focused_cem.arrows)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_get_manager(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)

        # Act
        returned_manager = ui_graph.get_manager()

        # Assert
        self.assertEqual(returned_manager, manager)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_get_current_cem_focused_cem_not_none(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = MagicMock()

        # Act
        current_cem = ui_graph.get_current_cem()

        # Assert
        self.assertEqual(current_cem, ui_graph.focused_cem)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_get_current_cem_focused_cem_none(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)
        ui_graph.focused_cem = None

        # Act
        current_cem = ui_graph.get_current_cem()

        # Assert
        self.assertEqual(current_cem, ui_graph.full_cem)

    @patch('src.view.ui_graph.CanvasElementManager')
    def test_resize(self, mock_canvas_element_manager):
        # Arrange
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        digraph = MagicMock()
        node_radius = 10
        panel_width = 100
        header_height = 50
        width = 800
        height = 600
        ui_graph = UIGraph(window, manager, width, height, node_radius, digraph, panel_width, header_height, colors)

        # Act
        new_width = 400
        new_height = 300
        new_window = MagicMock()
        new_manager = MagicMock()
        ui_graph.resize(new_width, new_height, new_window, new_manager)

        # Assert
        self.assertEqual(ui_graph.window, new_window)
        self.assertEqual(ui_graph.manager, new_manager)
        self.assertEqual(ui_graph.width, new_width)
        self.assertEqual(ui_graph.height, new_height)