import pygame as pg
import pygame_gui as pgui
import math

from src.view.canvas_element_manager import CanvasElementManager

import unittest
from unittest.mock import patch, MagicMock, call


class TestCanvasElementManager(unittest.TestCase):
    @patch('src.view.canvas_element_manager.Layout')
    def test_init(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)
        self.assertEqual(canvas_element_manager.digraph, digraph)
        self.assertEqual(canvas_element_manager.window, window)
        self.assertEqual(canvas_element_manager.manager, manager)
        self.assertEqual(canvas_element_manager.NODE_RADIUS, node_radius)
        self.assertEqual(canvas_element_manager.colors, colors)
        self.assertEqual(canvas_element_manager.focused, focused)
        self.assertEqual(canvas_element_manager.focused_node, focused_node)
        self.assertEqual(canvas_element_manager.focused_depth, focused_depth)
        self.assertEqual(canvas_element_manager.vertical_scatter, vertical_scatter)
        self.assertEqual(canvas_element_manager.horizontal_scatter, horizontal_scatter)
        self.assertIsNone(canvas_element_manager.selected_button)
        self.assertIsNone(canvas_element_manager.selected_arrow)
        self.assertEqual(canvas_element_manager.node_buttons, [])
        self.assertEqual(canvas_element_manager.arrows, [])
        mock_layout.assert_called_once_with(digraph, canvas_element_manager)

    @patch('src.view.canvas_element_manager.Layout')
    def test_move_all(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)
        dx = 1
        dy = 2
        node_button = MagicMock()
        canvas_element_manager.node_buttons = [(MagicMock(), node_button)]
        canvas_element_manager.move_all(dx, dy)
        node_button.move.assert_called_once_with(dx, dy)

    @patch('src.view.canvas_element_manager.Layout')
    def test_zoom_all(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)
        zoom_lvl = 2
        scale_factor = 2
        cursor_pos = (1, 2)
        node_button = MagicMock()
        arrow = MagicMock()
        canvas_element_manager.node_buttons = [(MagicMock(), node_button)]
        canvas_element_manager.arrows = [(MagicMock(), MagicMock(), arrow)]
        canvas_element_manager.zoom_all(zoom_lvl, scale_factor, cursor_pos)
        node_button.zoom.assert_called_once_with(zoom_lvl, scale_factor, cursor_pos)
        arrow.zoom.assert_called_once_with(scale_factor)

    @patch('src.view.canvas_element_manager.Layout')
    def test_change_colors(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)
        new_colors = MagicMock()
        node_button = MagicMock()
        arrow = MagicMock()
        canvas_element_manager.node_buttons = [(MagicMock(), node_button)]
        canvas_element_manager.arrows = [(MagicMock(), MagicMock(), arrow)]
        canvas_element_manager.change_colors(new_colors)
        node_button.change_colors.assert_called_once_with(new_colors)
        arrow.change_color.assert_called_once_with(new_colors['edge'])

    @patch('src.view.canvas_element_manager.Layout')
    def test_selected_node_changed(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)
        selected_button = MagicMock()
        node_button = MagicMock()
        canvas_element_manager.node_buttons = [(MagicMock(), selected_button)]
        canvas_element_manager.selected_button = None
        canvas_element_manager.selected_node_changed(selected_button)
        canvas_element_manager.selected_button = selected_button
        canvas_element_manager.selected_node_changed(selected_button)
        self.assertEqual(canvas_element_manager.selected_button, selected_button)
        canvas_element_manager.selected_node_changed(selected_button)

    @patch('src.view.canvas_element_manager.Layout')
    def test_selected_edge_changed(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)
        selected_arrow = MagicMock()
        arrow = MagicMock()
        canvas_element_manager.arrows = [(MagicMock(), MagicMock(), selected_arrow)]
        canvas_element_manager.selected_arrow = None
        canvas_element_manager.selected_edge_changed(selected_arrow)
        canvas_element_manager.selected_arrow = selected_arrow
        canvas_element_manager.selected_edge_changed(selected_arrow)
        self.assertEqual(canvas_element_manager.selected_arrow, selected_arrow)
        canvas_element_manager.selected_edge_changed(selected_arrow)

    @patch('src.view.canvas_element_manager.Layout')
    def test_searched_nodes_changed(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        selected_button = MagicMock()
        not_selected_button = MagicMock()
        node_buttons = [(MagicMock(), selected_button), (MagicMock(), not_selected_button)]
        canvas_element_manager.selected_button = selected_button
        canvas_element_manager.node_buttons = node_buttons
        mode = MagicMock()
        canvas_element_manager.searched_nodes_changed(None, mode)

        selected_button.change_colors.assert_called_once_with(colors, selected=True)
        not_selected_button.change_colors.assert_called_once_with(colors)

    @patch('src.view.canvas_element_manager.Layout')
    def test_searched_nodes_changed_filtered_info_id(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        selected_button = MagicMock()
        not_selected_button_1 = MagicMock()
        not_selected_node_1 = MagicMock()
        not_selected_node_1.id = 1
        not_selected_node_1.name = 'first'
        not_selected_button_2 = MagicMock()
        not_selected_node_2 = MagicMock()
        not_selected_node_2.id = 2
        not_selected_node_2.name = 'second'
        node_buttons = [(MagicMock(), selected_button), (not_selected_node_1, not_selected_button_1), (not_selected_node_2, not_selected_button_2)]
        canvas_element_manager.selected_button = selected_button
        canvas_element_manager.node_buttons = node_buttons
        filtered_info = [1]
        canvas_element_manager.searched_nodes_changed(filtered_info, 'id')

        selected_button.change_colors.assert_called_once_with(colors, selected=True)
        not_selected_button_1.change_colors.assert_called_once_with(colors, searched=True)
        not_selected_button_2.change_colors.assert_called_once_with(colors)

    @patch('src.view.canvas_element_manager.Layout')
    def test_searched_nodes_changed_filtered_info_name(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        selected_button = MagicMock()
        not_selected_button_1 = MagicMock()
        not_selected_node_1 = MagicMock()
        not_selected_node_1.id = 1
        not_selected_node_1.name = 'first'
        not_selected_button_2 = MagicMock()
        not_selected_node_2 = MagicMock()
        not_selected_node_2.id = 2
        not_selected_node_2.name = 'second'
        node_buttons = [(MagicMock(), selected_button), (not_selected_node_1, not_selected_button_1),
                        (not_selected_node_2, not_selected_button_2)]
        canvas_element_manager.selected_button = selected_button
        canvas_element_manager.node_buttons = node_buttons
        filtered_info = ['first']
        canvas_element_manager.searched_nodes_changed(filtered_info, 'name')

        selected_button.change_colors.assert_called_once_with(colors, selected=True)
        not_selected_button_1.change_colors.assert_called_once_with(colors, searched=True)
        not_selected_button_2.change_colors.assert_called_once_with(colors)

    @patch('src.view.canvas_element_manager.Layout')
    def test_unset_selected_node(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        selected_button = MagicMock()
        not_selected_button = MagicMock()
        node_buttons = [(MagicMock(), selected_button), (MagicMock(), not_selected_button)]
        canvas_element_manager.selected_button = selected_button
        canvas_element_manager.node_buttons = node_buttons
        canvas_element_manager.unset_selected_node()
        selected_button.change_colors.assert_called_once_with(colors)
        not_selected_button.change_colors.assert_not_called()

    @patch('src.view.canvas_element_manager.Layout')
    def test_unset_selected_edge(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        actual_arrow = MagicMock()
        selected_arrow = [None, None, actual_arrow]
        not_selected_arrow = MagicMock()
        arrows = [(MagicMock(), MagicMock(), selected_arrow), (MagicMock(), MagicMock(), not_selected_arrow)]
        canvas_element_manager.selected_arrow = selected_arrow
        canvas_element_manager.arrows = arrows
        canvas_element_manager.unset_selected_edge()
        actual_arrow.change_color.assert_called_once_with(colors['edge'])
        not_selected_arrow.change_color.assert_not_called()

    @patch('src.view.canvas_element_manager.Layout')
    def test_center_around_full_cem(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        node_button = MagicMock()
        node_button.x = 1
        node_button.y = 2
        canvas_element_manager.node_buttons = [(MagicMock(), node_button)]
        canvas_element_manager.center_around(None, None, full_cem=True)
        node_button.move.assert_called_once()

    @patch('src.view.canvas_element_manager.Layout')
    def test_center_around(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = None
        focused_node = None
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        node_button = MagicMock()
        node_button.x = 1
        node_button.y = 2
        canvas_element_manager.node_buttons = [(MagicMock(), node_button)]
        canvas_element_manager.center_around(1, 2)
        node_button.move.assert_called_once()

    @patch('src.view.canvas_element_manager.Layout')
    def test_update_focus(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = 2
        focused_node = MagicMock()
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        temp_cem = MagicMock()
        temp_cem.node_buttons = [(MagicMock(), MagicMock())]
        temp_cem.arrows = [(MagicMock(), MagicMock(), MagicMock())]

        with patch.object(canvas_element_manager, 'interpolate') as mock_interpolate:
            canvas_element_manager.update_focus(digraph, focused_depth, focused_node, vertical_scatter, horizontal_scatter)
            mock_interpolate.assert_called_once()

        self.assertEqual(canvas_element_manager.vertical_scatter, vertical_scatter)
        self.assertEqual(canvas_element_manager.horizontal_scatter, horizontal_scatter)
        self.assertEqual(canvas_element_manager.focused_depth, focused_depth)
        self.assertEqual(canvas_element_manager.focused_node, focused_node)

    @patch('src.view.canvas_element_manager.Layout')
    def test_draw_node_buttons(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = 2
        focused_node = MagicMock()
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        node_button = MagicMock()
        node_button.x = 1
        node_button.y = 2
        canvas_element_manager.node_buttons = [(MagicMock(), node_button)]
        canvas_element_manager.draw_node_buttons()
        node_button.draw.assert_called_once()

    @patch('src.view.canvas_element_manager.Layout')
    def test_draw_arrows(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = 2
        focused_node = MagicMock()
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        arrow = MagicMock()
        canvas_element_manager.arrows = [(MagicMock(), MagicMock(), arrow)]
        canvas_element_manager.draw_arrows()
        arrow.draw.assert_called_once()

    @patch('src.view.canvas_element_manager.Layout')
    def test_create_edges(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = 2
        focused_node = MagicMock()
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)

        with patch.object(canvas_element_manager, 'create_edges') as mock_create_edges:
            canvas_element_manager.create_edges()
            mock_create_edges.assert_called_once()
        self.assertEqual(len(canvas_element_manager.arrows), 0)

    @patch('src.view.canvas_element_manager.Layout')
    def test_create_arrow(self, mock_layout):
        digraph = MagicMock()
        window = MagicMock()
        manager = MagicMock()
        colors = MagicMock()
        node_radius = 15
        focused = False
        focused_depth = 2
        focused_node = MagicMock()
        vertical_scatter = 3
        horizontal_scatter = 3
        canvas_element_manager = CanvasElementManager(digraph, window, manager, colors, node_radius, focused,
                                                      focused_depth, focused_node, vertical_scatter, horizontal_scatter)
        button_start = MagicMock()
        button_end = MagicMock()
        arrow = MagicMock()
        edge = [MagicMock(), MagicMock()]
        with patch('src.view.canvas_element_manager.Arrow', return_value=arrow) as mock_arrow:
            canvas_element_manager.create_arrow(button_start, button_end, edge[0], edge[1], MagicMock())
            mock_arrow.assert_called_once()
        self.assertEqual(len(canvas_element_manager.arrows), 1)


if __name__ == '__main__':
    unittest.main()
