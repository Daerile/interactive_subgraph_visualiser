import pygame as pg
import pygame_gui as pgui

from src.view.ui_header import UIHeader
import unittest
from unittest.mock import patch, mock_open, MagicMock, call, PropertyMock

class TestUIHeader(unittest.TestCase):
    def setUp(self):
        self.patcher_create_base_panel = patch.object(UIHeader, 'create_base_panel')
        self.mock_create_base_panel = self.patcher_create_base_panel.start()

        self.patcher_create_buttons = patch.object(UIHeader, 'create_buttons')
        self.mock_create_buttons = self.patcher_create_buttons.start()

        self.patcher_pgui_elements = patch('pygame_gui.elements')
        self.mock_pgui_elements = self.patcher_pgui_elements.start()

    def tearDown(self):
        self.patcher_create_base_panel.stop()
        self.patcher_create_buttons.stop()
        self.patcher_pgui_elements.stop()

    def test_init(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        self.assertEqual(header.window, window)
        self.assertEqual(header.manager, manager)
        self.assertEqual(header.digraph, digraph)
        self.assertEqual(header.width, 400)
        self.assertEqual(header.height, 300)
        self.assertIsNone(header.menu_points)
        self.assertIsNone(header.menu_buttons)
        self.assertIsNone(header.text_box)
        self.assertIsNone(header.popup)
        self.assertIsNone(header.load_popup)
        self.assertIsNone(header.load_popup_items)
        self.mock_create_base_panel.assert_called_once()
        self.mock_create_buttons.assert_called_once()

    def test_create_buttons(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        self.patcher_create_buttons.stop()
        self.mock_pgui_elements.UIButton.side_effect = [1, 2, 3]
        header.create_buttons()
        self.assertEqual(header.load_button, 1)
        self.assertEqual(header.save_button, 2)
        self.assertEqual(header.help_button, 3)

    def test_create_base_panel(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        self.patcher_create_base_panel.stop()
        self.mock_pgui_elements.UIPanel.return_value = 1
        ret_val = header.create_base_panel()
        self.assertEqual(ret_val, 1)

    def test_handle_help_button_pressed(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        mock_popup = MagicMock()
        self.mock_pgui_elements.UIWindow.return_value = mock_popup
        self.mock_pgui_elements.UITextBox.return_value = 2
        header.handle_help_button_pressed()
        self.assertEqual(header.popup, mock_popup)
        mock_popup.set_blocking.assert_called_once_with(True)
        self.assertEqual(header.text_box, 2)
        self.assertEqual(len(header.menu_points.keys()), 9)

    def test_handle_menu_button_pressed(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        header.menu_points = {
            'menu1': 'menu1',
            'menu2': 'menu2'
        }
        header.menu_buttons = {
            'menu1': 'menu1',
            'menu2': 'menu2'
        }
        mock_text_box = MagicMock()
        header.text_box = mock_text_box
        mock_button = MagicMock()
        mock_button.text = 'menu1'
        header.handle_menu_button_pressed(mock_button)
        mock_text_box.set_text.assert_called_once_with('menu1')
        self.assertEqual(header.menu_points['menu1'], 'menu1')
        self.assertEqual(header.menu_buttons['menu1'], 'menu1')
        self.assertEqual(header.menu_points['menu2'], 'menu2')
        self.assertEqual(header.menu_buttons['menu2'], 'menu2')

    def test_handle_load_button_pressed(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        mock_popup = MagicMock()
        self.mock_pgui_elements.UIWindow.return_value = mock_popup
        self.mock_pgui_elements.UIList.return_value = 2
        mock_load_popup = MagicMock()
        header.handle_load_button_pressed(["alma"])
        self.assertEqual(header.load_popup, mock_popup)
        mock_popup.set_blocking.assert_called_once_with(True)
        self.assertEqual(len(header.load_popup_items), 5)

    def test_handle_must_have_dropdown_changed(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        mock_dropdown_1 = MagicMock()
        mock_dropdown_2 = MagicMock()
        mock_dropdown_1.selected_option = ['None']
        mock_dropdown_2.selected_option = ['Column1']
        mock_okay_button = MagicMock()
        mock_status_label = MagicMock()
        header.load_popup_items = {
            'must_have': [mock_dropdown_1, mock_dropdown_2],
            'optional': [],
            'okay_button': mock_okay_button,
            'status_label': mock_status_label
        }
        header.handle_must_have_dropdown_changed()
        mock_okay_button.disable.assert_called_once()
        self.assertEqual(mock_status_label.set_text.call_count, 1)

        mock_dropdown_1.selected_option = ['Column1']
        mock_dropdown_2.selected_option = ['Column1']
        header.handle_must_have_dropdown_changed()
        self.assertEqual(mock_okay_button.disable.call_count, 2)
        self.assertEqual(mock_status_label.set_text.call_count, 2)

        mock_dropdown_1.selected_option = ['Column1']
        mock_dropdown_2.selected_option = ['Column2']
        header.handle_must_have_dropdown_changed()
        mock_okay_button.enable.assert_called_once()
        self.assertEqual(mock_status_label.set_text.call_count, 3)

    def test_handle_load_popup_okay_button_pressed(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        mock_dropdown_1 = MagicMock()
        mock_dropdown_2 = MagicMock()
        mock_dropdown_3 = MagicMock()
        mock_dropdown_4 = MagicMock()
        mock_dropdown_5 = MagicMock()
        mock_dropdown_1.selected_option = ['Column1']
        mock_dropdown_2.selected_option = ['Column2']
        mock_dropdown_3.selected_option = ['Column3']
        mock_dropdown_4.selected_option = ['Column4']
        mock_dropdown_5.selected_option = ['Column5']
        mock_load_popup = MagicMock()
        header.load_popup = mock_load_popup
        header.load_popup_items = {
            'must_have': [mock_dropdown_1, mock_dropdown_2, mock_dropdown_3],
            'optional': [mock_dropdown_4, mock_dropdown_5]
        }
        must_have_pairings, optional_pairings = header.handle_load_popup_okay_button_pressed()
        mock_load_popup.kill.assert_called_once()
        self.assertEqual(must_have_pairings, {
            'node_id': 'Column1',
            'sub_id': 'Column2',
            'connections': 'Column3'
        })
        self.assertEqual(optional_pairings, {
            'node_name': 'Column4',
            'sub_id_value_name': 'Column5'
        })

    def test_resize(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        mock_killall = MagicMock()
        mock_create_base_panel = MagicMock()
        mock_create_buttons = MagicMock()
        header.killall = mock_killall
        header.create_base_panel = mock_create_base_panel
        header.create_buttons = mock_create_buttons
        header.resize(500, 600, window, manager)
        mock_killall.assert_called_once()
        mock_create_base_panel.assert_called_once()
        mock_create_buttons.assert_called_once()
        self.assertEqual(header.window, window)
        self.assertEqual(header.manager, manager)
        self.assertEqual(header.width, 500)
        self.assertEqual(header.height, 600)

    def test_handle_load_popup_cancel_button_pressed(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        mock_load_popup = MagicMock()
        header.load_popup = mock_load_popup
        header.handle_load_popup_cancel_button_pressed()
        mock_load_popup.kill.assert_called_once()

    def test_killall(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        mock_load_button = MagicMock()
        mock_save_button = MagicMock()
        mock_help_button = MagicMock()
        mock_base_panel = MagicMock()
        header.load_button = mock_load_button
        header.save_button = mock_save_button
        header.help_button = mock_help_button
        header.base_panel = mock_base_panel
        header.killall()
        mock_load_button.kill.assert_called_once()
        mock_save_button.kill.assert_called_once()
        mock_help_button.kill.assert_called_once()
        mock_base_panel.kill.assert_called_once()

    def test_process_events(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        mock_event = MagicMock()
        header.process_events(mock_event)
        manager.process_events.assert_called_once_with(mock_event)

    def test_draw_ui(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        header.draw_ui()
        manager.draw_ui.assert_called_once_with(window)

    def test_get_manager(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        self.assertEqual(header.get_manager(), manager)

    def test_update(self):
        window = MagicMock()
        manager = MagicMock()
        digraph = MagicMock()
        header = UIHeader(window, manager, 400, 300, digraph)
        time_delta = 0.1
        header.update(time_delta)
        manager.update.assert_called_once_with(time_delta)

if __name__ == '__main__':
    unittest.main()