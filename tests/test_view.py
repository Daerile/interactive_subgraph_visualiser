import pygame as pg
import networkx as nx

from src.view.view import View
import unittest
from unittest.mock import patch, mock_open, MagicMock, call, PropertyMock


class TestView(unittest.TestCase):

    def setUp(self):
        self.patcher_pg = patch('src.view.view.pg')
        self.mock_pg = self.patcher_pg.start()

        self.patcher_view_model = patch('src.view.view.ViewModel')
        self.mock_view_model = self.patcher_view_model.start()

        self.patcher_json = patch('src.view.view.json')
        self.mock_json = self.patcher_json.start()

        self.patcher_ui_header = patch('src.view.view.UIHeader')
        self.mock_ui_header = self.patcher_ui_header.start()

        self.patcher_ui_graph = patch('src.view.view.UIGraph')
        self.mock_ui_graph = self.patcher_ui_graph.start()

        self.patcher_ui_panel = patch('src.view.view.UIPanel')
        self.mock_ui_panel = self.patcher_ui_panel.start()

        self.patcher_pgui = patch('src.view.view.pgui')
        self.mock_pgui = self.patcher_pgui.start()

    def tearDown(self):
        self.patcher_pg.stop()
        self.patcher_view_model.stop()
        self.patcher_json.stop()
        self.patcher_ui_header.stop()
        self.patcher_ui_graph.stop()
        self.patcher_ui_panel.stop()
        self.patcher_pgui.stop()

    @patch('builtins.open', new_callable=mock_open)
    def test_init_focused(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.handle_light_mode_pressed.return_value = {}
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

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

        self.mock_pg.init.assert_called_once()
        self.mock_view_model.assert_called_once()
        self.mock_pg.display.set_mode.assert_called_once()
        self.mock_json.load.assert_called_once()
        self.mock_json.dump.assert_called_once()
        self.mock_pgui.UIManager.assert_called_once()
        self.mock_ui_panel.assert_called_once_with(
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
        self.mock_ui_header.assert_called_once_with(
            view.window,
            view.manager,
            view.HEADER_WIDTH,
            view.HEADER_HEIGHT,
            view.digraph
        )
        self.mock_ui_graph.assert_called_once_with(
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
        self.mock_pg.display.set_caption.assert_called_once_with("Interactive Subgraph Visualiser")

    @patch('builtins.open', new_callable=mock_open)
    def test_init_no_focused(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.handle_light_mode_pressed.return_value = {}
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

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

        self.mock_pg.init.assert_called_once()
        self.mock_view_model.assert_called_once()
        self.mock_pg.display.set_mode.assert_called_once()
        self.mock_json.load.assert_called_once()
        self.mock_json.dump.assert_called_once()
        self.mock_pgui.UIManager.assert_called_once()
        self.mock_ui_panel.assert_called_once_with(
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
        self.mock_ui_header.assert_called_once_with(
            view.window,
            view.manager,
            view.HEADER_WIDTH,
            view.HEADER_HEIGHT,
            view.digraph
        )
        self.mock_ui_graph.assert_called_once_with(
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
        self.mock_pg.display.set_caption.assert_called_once_with("Interactive Subgraph Visualiser")

    @patch('builtins.open', new_callable=mock_open)
    def test_digraph_loaded(self, mock_open):
        digraph = MagicMock()
        optional_pairings = []

        mock_ui_graph_return_val = MagicMock()
        mock_ui_graph_return_val.digraph_loaded.return_value = {}
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        view = View(digraph)
        with patch.object(view, 'run', return_value=None):
            view.digraph_loaded(optional_pairings)

        self.assertEqual(view.zoom_lvl, 0)

        self.mock_ui_panel.assert_called_with(
            view.window,
            view.manager,
            view.PANEL_WIDTH,
            view.PANEL_HEIGHT,
            view.digraph,
            2,
            3,
            3,
            view.HEADER_HEIGHT,
            colors=view.colors,
            optional_pairings=optional_pairings
        )
        mock_ui_graph_return_val.digraph_loaded.assert_called_once_with(view.digraph)
        self.mock_ui_header.assert_called_with(
            view.window,
            view.manager,
            view.HEADER_WIDTH,
            view.HEADER_HEIGHT,
            view.digraph
        )
        self.mock_pg.display.update.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_focus_changed(self, mock_open):
        # Setup
        digraph = MagicMock()
        view = View(digraph)

        # Mock required attributes and methods
        mock_ui_panel_instance = self.mock_ui_panel.return_value
        mock_ui_panel_instance.get_focused_depth.return_value = 2
        mock_ui_panel_instance.get_horizontal_scatter.return_value = 3
        mock_ui_panel_instance.get_vertical_scatter.return_value = 3
        mock_ui_panel_instance.closed = False
        mock_ui_panel_instance.optional_pairings = ['pair1', 'pair2']

        focused_digraph = nx.DiGraph()

        # Mock self.run to prevent it from executing
        with patch.object(view, 'run', return_value=None):
            view.focus_changed(focused_digraph)

        # Assertions to ensure the focus_changed method functions correctly
        self.assertEqual(view.zoom_lvl, 0)
        mock_ui_panel_instance.killall.assert_called_once()
        self.mock_ui_panel.assert_called_with(
            view.window,
            view.manager,
            view.PANEL_WIDTH,
            view.PANEL_HEIGHT,
            focused_digraph,
            2,
            3,
            3,
            view.HEADER_HEIGHT,
            colors=view.colors,
            optional_pairings=['pair1', 'pair2']
        )
        mock_ui_panel_instance.update.assert_called_once_with(0)
        mock_ui_panel_instance.draw_ui.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_light_mode_pressed(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.handle_light_mode_pressed.side_effect = [{}, {}]
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_graph_return_val = MagicMock()
        mock_ui_graph_return_val.change_colors.return_value = {}
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        view = View(digraph)
        view.light_mode_pressed()

        mock_ui_panel_return_val.handle_light_mode_pressed.assert_has_calls([call(), call()])

        self.assertEqual(view.colors, {})
        mock_ui_graph_return_val.change_colors.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_dark_mode_pressed(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.handle_light_mode_pressed.return_value = {}
        mock_ui_panel_return_val.handle_dark_mode_pressed.return_value = {}
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_graph_return_val = MagicMock()
        mock_ui_graph_return_val.change_colors.return_value = {}
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        view = View(digraph)
        view.dark_mode_pressed()

        mock_ui_panel_return_val.handle_light_mode_pressed.assert_called_once()
        mock_ui_panel_return_val.handle_dark_mode_pressed.assert_called_once()

        self.assertEqual(view.colors, {})
        mock_ui_graph_return_val.change_colors.assert_called_once()


    @patch('builtins.open', new_callable=mock_open)
    def test_personal_mode_pressed(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.handle_light_mode_pressed.return_value = {}
        mock_ui_panel_return_val.handle_personal_mode_pressed.return_value = {}
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_graph_return_val = MagicMock()
        mock_ui_graph_return_val.change_colors.return_value = {}
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        view = View(digraph)
        view.personal_mode_pressed()

        mock_ui_panel_return_val.handle_light_mode_pressed.assert_called_once()
        mock_ui_panel_return_val.handle_personal_mode_pressed.assert_called_once()

        self.assertEqual(view.colors, {})
        mock_ui_graph_return_val.change_colors.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_node_button_clicked(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.update_information_box.return_value = {}
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_graph_return_val = MagicMock()
        mock_ui_graph_return_val.handle_node_selected.return_value = {}
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        param = MagicMock()
        param.node = {}
        view = View(digraph)
        view.node_button_clicked(param)

        mock_ui_panel_return_val.update_information_box.assert_called_once_with(param.node)
        mock_ui_graph_return_val.handle_node_selected.assert_called_once_with(param)

    @patch('builtins.open', new_callable=mock_open)
    def test_edge_clicked(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.update_information_box.return_value = {}
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_graph_return_val = MagicMock()
        mock_ui_graph_return_val.handle_edge_selected.return_value = {}
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        param = MagicMock()
        view = View(digraph)
        view.edge_clicked(param)

        mock_ui_panel_return_val.update_information_box.assert_called_once_with(param, edge=True)
        mock_ui_graph_return_val.handle_edge_selected.assert_called_once_with(param)

    @patch('builtins.open', new_callable=mock_open)
    def test_run(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.update.return_value = None
        mock_ui_panel_return_val.draw_ui.return_value = None
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_graph_return_val = MagicMock()
        mock_ui_graph_return_val.update.return_value = None
        mock_ui_graph_return_val.draw_ui.return_value = None
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.update.return_value = None
        mock_ui_header_return_val.draw_ui.return_value = None
        self.mock_ui_header.return_value = mock_ui_header_return_val

        view = View(digraph)
        with patch.object(view, 'handle_events', return_value=False):
            with self.assertRaises(SystemExit):
                view.run()

        mock_ui_panel_return_val.update.assert_called_once()
        mock_ui_panel_return_val.draw_ui.assert_called_once()
        mock_ui_graph_return_val.update.assert_called_once()
        mock_ui_graph_return_val.draw_ui.assert_called_once()
        mock_ui_header_return_val.update.assert_called_once()
        mock_ui_header_return_val.draw_ui.assert_called_once()

        self.mock_pg.display.update.assert_called_once()
        self.mock_pg.quit.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_event_quit(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.process_events.return_value = None
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        view = View(digraph)

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.QUIT
        self.mock_pg.event.get.return_value = [mock_event]
        view.handle_events()

        mock_ui_panel_return_val.process_events.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_event_resize(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_header_return_val = MagicMock()
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_ui_graph_return_val = MagicMock()
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.VIDEORESIZE
        mock_event.w = 500
        mock_event.h = 300
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        self.assertEqual(view.WIDTH, 500)
        self.assertEqual(view.HEIGHT, 300)
        self.assertEqual(view.HEADER_WIDTH, 500)
        self.assertEqual(view.HEADER_HEIGHT, 35)
        self.assertEqual(view.PANEL_WIDTH, 380)
        self.assertEqual(view.PANEL_HEIGHT, 300 - 35 + 5)
        self.assertEqual(view.GRAPH_WIDTH, 500 - 380 + 5)
        self.assertEqual(view.GRAPH_HEIGHT, 300 - 35 + 5)

        self.assertEqual([c[0][0] for c in self.mock_pg.display.set_mode.call_args_list], [(1280, 720), (500, 300)])
        self.assertEqual([c[0][0] for c in self.mock_pgui.UIManager.call_args_list], [(1280, 720), (500, 300)])
        mock_ui_panel_return_val.resize.assert_called_once()
        mock_ui_header_return_val.resize.assert_called_once()
        mock_ui_graph_return_val.resize.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_mouse_button_down_button(self, mock_open):
        digraph = MagicMock()

        mock_ui_graph_return_val = MagicMock()
        mock_get_node_buttons = MagicMock()
        mock_get_node_buttons.handle_click.return_value = 1
        mock_get_node_buttons.x = -1
        mock_get_node_buttons.y = -2
        mock_ui_graph_return_val.get_node_buttons.return_value = [(None, mock_get_node_buttons)]
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.popup = None
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.popup = None
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.MOUSEBUTTONDOWN
        mock_event.button = 1
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        self.assertEqual(view.dragged_button, mock_get_node_buttons)
        self.assertEqual(view.dragged_button_x, -1)
        self.assertEqual(view.dragged_button_y, -2)
        self.assertEqual(view.res, 1)

        mock_ui_graph_return_val.get_node_buttons.assert_called_once()
        mock_get_node_buttons.handle_click.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_mouse_button_down_edge(self, mock_open):
        digraph = MagicMock()

        mock_ui_graph_return_val = MagicMock()
        mock_get_arrows = MagicMock()
        mock_get_arrows.handle_click.return_value = 1
        mock_ui_graph_return_val.get_arrows.return_value = [(None, None, mock_get_arrows)]
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.popup = None
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.popup = None
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.MOUSEBUTTONDOWN
        mock_event.button = 1
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        with patch.object(view, 'edge_clicked', return_value=None) as mock_edge_clicked:
            view.handle_events()
            mock_edge_clicked.assert_called_once()

        mock_ui_graph_return_val.get_arrows.assert_called_once()
        mock_get_arrows.handle_click.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_mouse_button_down_neither_1(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.popup = None
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.popup = None
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.MOUSEBUTTONDOWN
        mock_event.button = 1
        mock_event.pos = (500, 200)
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        self.assertEqual(view.dragging, True)
        self.assertEqual(view.offset_x, 500)
        self.assertEqual(view.offset_y, 200)

    @patch('builtins.open', new_callable=mock_open)
    def test_mouse_button_down_neither_4(self, mock_open):
        digraph = MagicMock()

        mock_ui_graph_return_val = MagicMock()
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.popup = None
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.popup = None
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.MOUSEBUTTONDOWN
        mock_event.button = 4
        mock_event.pos = (500, 200)
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        self.assertEqual(view.zoom_lvl, 1)
        self.assertEqual(view.zoom_scale, 1.1 ** 1)
        mock_ui_graph_return_val.zoom_all.assert_called_once_with(1, 1.1, (500, 200))

    @patch('builtins.open', new_callable=mock_open)
    def test_mouse_button_down_neither_5(self, mock_open):
        digraph = MagicMock()

        mock_ui_graph_return_val = MagicMock()
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.popup = None
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.popup = None
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.MOUSEBUTTONDOWN
        mock_event.button = 5
        mock_event.pos = (500, 200)
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        self.assertEqual(view.zoom_lvl, -1)
        self.assertEqual(view.zoom_scale, 1.1 ** -1)
        mock_ui_graph_return_val.zoom_all.assert_called_once_with(-1, 100 / 110, (500, 200))

    @patch('builtins.open', new_callable=mock_open)
    def test_mouse_button_up_res1(self, mock_open):
        digraph = MagicMock()

        mock_ui_graph_return_val = MagicMock()
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_ui_panel_return_val = MagicMock()
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_header_return_val = MagicMock()
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.MOUSEBUTTONUP
        mock_event.button = 1
        self.mock_pg.event.get.return_value = [mock_event]

        mock_dragged_button = MagicMock()
        mock_dragged_button.x = 500
        mock_dragged_button.y = 300

        view = View(digraph)
        view.dragged_button = mock_dragged_button
        view.dragged_button_x = 500
        view.dragged_button_y = 300
        view.res = 1
        with patch.object(view, 'node_button_clicked', return_value=None) as mock_node_button_clicked:
            view.handle_events()
            mock_node_button_clicked.assert_called_once()

        self.assertIsNone(view.dragged_button)
        self.assertIsNone(view.res)

    @patch('builtins.open', new_callable=mock_open)
    def test_mouse_button_up_res2(self, mock_open):
        digraph = MagicMock()

        mock_ui_graph_return_val = MagicMock()
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_ui_panel_return_val = MagicMock()
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_view_model_return_val = MagicMock()
        self.mock_view_model.return_value = mock_view_model_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.MOUSEBUTTONUP
        mock_event.button = 1
        self.mock_pg.event.get.return_value = [mock_event]

        mock_dragged_button = MagicMock()
        mock_dragged_button.x = 500
        mock_dragged_button.y = 300

        view = View(digraph)
        view.dragged_button = mock_dragged_button
        view.dragged_button_x = 500
        view.dragged_button_y = 300
        view.res = 2
        with patch.object(view, 'focus_changed', return_value=None) as mock_focus_changed:
            view.handle_events()
            mock_focus_changed.assert_called_once()

        self.assertIsNone(view.res)

        mock_ui_panel_return_val.get_focused_depth.assert_called_once()
        mock_ui_panel_return_val.get_vertical_scatter.assert_called_once()
        mock_ui_panel_return_val.get_horizontal_scatter.assert_called_once()
        mock_view_model_return_val.handle_node_focused.assert_called_once()
        mock_ui_graph_return_val.handle_node_focused.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_mouse_motion_dragged_button(self, mock_open):
        digraph = MagicMock()

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.MOUSEMOTION
        mock_event.pos = (500, 400)
        self.mock_pg.event.get.return_value = [mock_event]

        mock_dragged_button = MagicMock()
        mock_dragged_button.x = 200
        mock_dragged_button.y = 300

        view = View(digraph)
        view.dragged_button = mock_dragged_button
        view.dragged_button_x = 200
        view.dragged_button_y = 300
        view.handle_events()

        mock_dragged_button.set_position.assert_called_once_with(500, 400)

    @patch('builtins.open', new_callable=mock_open)
    def test_mouse_motion_dragging(self, mock_open):
        digraph = MagicMock()

        mock_ui_graph_return_val = MagicMock()
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pg.MOUSEMOTION
        mock_event.pos = (500, 400)
        self.mock_pg.event.get.return_value = [mock_event]


        view = View(digraph)
        view.dragging = True
        view.handle_events()

        self.assertEqual(view.offset_x, 500)
        self.assertEqual(view.offset_y, 400)
        mock_ui_graph_return_val.move_all.called_once_with(500, 400)

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_search_by_id(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {'search_by_id_button': 'search_by_id_button'}
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'search_by_id_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_panel_return_val.handle_search_by_id_button_pressed.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_search_by_name(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button'
        }
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'search_by_name_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_panel_return_val.handle_search_by_name_button_pressed.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_close_button(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button'
        }
        mock_ui_panel_return_val.close_button = 'close_button'
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'close_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_panel_return_val.handle_close_button_pressed.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_dark_mode(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button'
        }
        mock_ui_panel_return_val.edit_box = {
            'light_mode': 'light_mode',
            'dark_mode': 'dark_mode'
        }
        mock_ui_panel_return_val.close_button = 'close_button'
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'dark_mode'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        with patch.object(view, 'dark_mode_pressed', return_value=None) as mock_dark_mode:
            view.handle_events()
            mock_dark_mode.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_light_mode(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button'
        }
        mock_ui_panel_return_val.edit_box = {
            'light_mode': 'light_mode',
            'dark_mode': 'dark_mode'
        }
        mock_ui_panel_return_val.close_button = 'close_button'
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'light_mode'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        with patch.object(view, 'light_mode_pressed', return_value=None) as mock_light_mode:
            view.handle_events()
            mock_light_mode.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_personal_mode(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button'
        }
        mock_ui_panel_return_val.edit_box = {
            'light_mode': 'light_mode',
            'dark_mode': 'dark_mode',
            'personal_mode': 'personal_mode'
        }
        mock_ui_panel_return_val.close_button = 'close_button'
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'personal_mode'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        with patch.object(view, 'personal_mode_pressed', return_value=None) as mock_personal_mode:
            view.handle_events()
            mock_personal_mode.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_switch_search(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button'
        }
        mock_ui_panel_return_val.edit_box = {
            'light_mode': 'light_mode',
            'dark_mode': 'dark_mode',
            'personal_mode': 'personal_mode'
        }
        mock_ui_panel_return_val.switch_panel = {
            'search': 'switch_search'
        }
        mock_ui_panel_return_val.close_button = 'close_button'
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'switch_search'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_panel_return_val.handle_switch_search_pressed.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_switch_edit(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button'
        }
        mock_ui_panel_return_val.edit_box = {
            'light_mode': 'light_mode',
            'dark_mode': 'dark_mode',
            'personal_mode': 'personal_mode'
        }
        mock_ui_panel_return_val.switch_panel = {
            'search': 'switch_search',
            'edit': 'switch_edit'
        }
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'switch_edit'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_panel_return_val.handle_switch_edit_pressed.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_return_button(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button',
            'return_button': 'return_button'
        }
        mock_ui_panel_return_val.edit_box = {
            'light_mode': 'light_mode',
            'dark_mode': 'dark_mode',
            'personal_mode': 'personal_mode'
        }
        mock_ui_panel_return_val.switch_panel = {
            'search': 'switch_search',
            'edit': 'switch_edit'
        }
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_graph_return_val = MagicMock()
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'return_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        with patch.object(view, 'focus_changed', return_value=None) as mock_focus_changed:
            view.handle_events()
            mock_focus_changed.assert_called_once()

        mock_ui_graph_return_val.handle_return_button_pressed.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_show_popup_button(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button',
            'return_button': 'return_button'
        }
        mock_ui_panel_return_val.edit_box = {
            'light_mode': 'light_mode',
            'dark_mode': 'dark_mode',
            'personal_mode': 'personal_mode'
        }
        mock_ui_panel_return_val.switch_panel = {
            'search': 'switch_search',
            'edit': 'switch_edit'
        }
        mock_ui_panel_return_val.infos = {'show_popup_button': 'show_popup_button'}
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'show_popup_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_panel_return_val.handle_popup_button_pressed.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_focus_button(self, mock_open):
        digraph = MagicMock()

        mock_ui_graph_return_val = MagicMock()
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_view_model_return_val = MagicMock()
        self.mock_view_model.return_value = mock_view_model_return_val

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {
            'search_by_id_button': 'search_by_id_button',
            'search_by_name_button': 'search_by_name_button',
            'return_button': 'return_button',
            'focus_button': 'focus_button'
        }
        mock_ui_panel_return_val.edit_box = {
            'light_mode': 'light_mode',
            'dark_mode': 'dark_mode',
            'personal_mode': 'personal_mode'
        }
        mock_ui_panel_return_val.switch_panel = {
            'search': 'switch_search',
            'edit': 'switch_edit'
        }
        mock_ui_panel_return_val.infos = {'show_popup_button': 'show_popup_button'}
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'focus_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        with patch.object(view, 'focus_changed', return_value=None) as mock_focus_changed:
            view.handle_events()
            mock_focus_changed.assert_called_once()

        mock_ui_panel_return_val.handle_focus_button_pressed.assert_called_once()
        mock_ui_panel_return_val.get_focused_depth.assert_called_once()
        mock_ui_panel_return_val.get_vertical_scatter.assert_called_once()
        mock_ui_panel_return_val.get_horizontal_scatter.assert_called_once()
        mock_view_model_return_val.handle_node_focused.assert_called_once()
        mock_ui_graph_return_val.handle_node_focused.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_load_button(self, mock_open):
        digraph = MagicMock()

        mock_view_model_return_val = MagicMock()
        mock_view_model_return_val.handle_load_button_pressed.return_value = 'alma'
        self.mock_view_model.return_value = mock_view_model_return_val

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.load_button = 'load_button'
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'load_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.view_model = mock_view_model_return_val
        view.handle_events()

        mock_ui_header_return_val.handle_load_button_pressed.assert_called_once_with('alma')
        mock_view_model_return_val.handle_load_button_pressed.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_save_button(self, mock_open):
        digraph = MagicMock()

        mock_view_model_return_val = MagicMock()
        self.mock_view_model.return_value = mock_view_model_return_val

        mock_ui_graph_return_val = MagicMock()
        mock_ui_graph_return_val.get_focused_digraph.return_value = 'alma'
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.save_button = 'save_button'
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'save_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.view_model = mock_view_model_return_val
        view.handle_events()

        mock_ui_graph_return_val.get_focused_digraph.assert_called_once()
        mock_view_model_return_val.handle_load_button_pressed.handle_save_button_pressed('alma')

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_help_button(self, mock_open):
        digraph = MagicMock()

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.help_button = 'help_button'
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'help_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_header_return_val.handle_help_button_pressed.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_menu_button(self, mock_open):
        digraph = MagicMock()

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.menu_buttons = {'menu_button': 'menu_button'}
        mock_ui_header_return_val.menu_button = 'menu_button'
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'menu_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_header_return_val.handle_menu_button_pressed.assert_called_once_with('menu_button')

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_button_pressed_load_okay(self, mock_open):
        digraph = MagicMock()

        mock_view_model_return_val = MagicMock()
        mock_view_model_return_val.create_digraph.return_value = 'alma'
        self.mock_view_model.return_value = mock_view_model_return_val

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.handle_load_popup_okay_button_pressed.return_value = ('alma', 'korte')
        mock_ui_header_return_val.load_popup_okay_button = 'load_popup_okay_button'
        mock_ui_header_return_val.load_popup_items = {'okay_button': 'load_popup_okay_button'}
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_BUTTON_PRESSED
        mock_event.ui_element = 'load_popup_okay_button'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        with patch.object(view, 'digraph_loaded', return_value=False) as mock_digraph_loaded:
            view.handle_events()
            mock_digraph_loaded.assert_called_once_with('korte')

        self.assertEqual(view.digraph, 'alma')

        mock_ui_header_return_val.handle_load_popup_okay_button_pressed.assert_called_once()
        mock_view_model_return_val.create_digraph.assert_called_once_with('alma', 'korte')

    @patch('builtins.open', new_callable=mock_open)
    def test_text_entry_changed_search_bar(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.search_box = {'search_text': 'search_text'}
        mock_ui_panel_return_val.handle_search_bar_changed.return_value = ('valami', 'read')
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_ui_graph_return_val = MagicMock()
        self.mock_ui_graph.return_value = mock_ui_graph_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_TEXT_ENTRY_CHANGED
        mock_event.ui_element = 'search_text'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_panel_return_val.handle_search_bar_changed.assert_called_once()
        mock_ui_graph_return_val.handle_searched_nodes_changed.assert_called_once_with('valami', 'read')

    @patch('builtins.open', new_callable=mock_open)
    def test_window_close_panel_popup(self, mock_open):
        digraph = MagicMock()

        mock_ui_panel_return_val = MagicMock()
        mock_ui_panel_return_val.popup = 'popup'
        self.mock_ui_panel.return_value = mock_ui_panel_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_WINDOW_CLOSE
        mock_event.ui_element = 'popup'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        self.assertIsNone(view.ui_panel.popup)

    @patch('builtins.open', new_callable=mock_open)
    def test_window_close_header_popup(self, mock_open):
        digraph = MagicMock()

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.popup = 'popup'
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_WINDOW_CLOSE
        mock_event.ui_element = 'popup'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        self.assertIsNone(view.ui_header.popup)

    @patch('builtins.open', new_callable=mock_open)
    def test_ui_drop_down_menu_changed_ui_header(self, mock_open):
        digraph = MagicMock()

        mock_ui_header_return_val = MagicMock()
        mock_ui_header_return_val.load_popup_items = {'must_have': 'popup', 'optional': 'something'}
        self.mock_ui_header.return_value = mock_ui_header_return_val

        mock_event = MagicMock()
        mock_event.type = self.mock_pgui.UI_DROP_DOWN_MENU_CHANGED
        mock_event.ui_element = 'popup'
        self.mock_pg.event.get.return_value = [mock_event]

        view = View(digraph)
        view.handle_events()

        mock_ui_header_return_val.handle_must_have_dropdown_changed.assert_called_once()
