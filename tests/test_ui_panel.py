import unittest
from unittest.mock import MagicMock, Mock, patch
from src.view.ui_panel import UIPanel
import pygame_gui as pgui
import pygame as pg


class TestUIPanel(unittest.TestCase):
    def setUp(self):
        self.patcher_pgui_elements = patch('src.view.ui_panel.pgui.elements')
        self.mock_pgui_elements = self.patcher_pgui_elements.start()

        self.patcher_create_base_panel = patch.object(UIPanel, 'create_base_panel')
        self.mock_create_base_panel = self.patcher_create_base_panel.start()

        self.patcher_create_switch_panel = patch.object(UIPanel, 'create_switch_panel')
        self.mock_create_switch_panel = self.patcher_create_switch_panel.start()

        self.patcher_create_information_box = patch.object(UIPanel, 'create_information_box')
        self.mock_create_information_box = self.patcher_create_information_box.start()

        self.patcher_create_search_box = patch.object(UIPanel, 'create_search_box')
        self.mock_create_search_box = self.patcher_create_search_box.start()

        self.patcher_create_edit_box = patch.object(UIPanel, 'create_edit_box')
        self.mock_create_edit_box = self.patcher_create_edit_box.start()

        self.patcher_create_action_information_box = patch.object(UIPanel, 'create_action_information_box')
        self.mock_create_action_information_box = self.patcher_create_action_information_box.start()

        self.patcher_create_close_button = patch.object(UIPanel, 'create_close_button')
        self.mock_create_close_button = self.patcher_create_close_button.start()

        self.mock_window = MagicMock()
        self.mock_manager = MagicMock()
        self.mock_digraph = MagicMock()
        self.ui_panel = UIPanel(self.mock_window, self.mock_manager, 1000, 800, self.mock_digraph, 3, 3, 3, 100)

    def tearDown(self):
        self.patcher_pgui_elements.stop()
        self.patcher_create_base_panel.stop()
        self.patcher_create_switch_panel.stop()
        self.patcher_create_information_box.stop()
        self.patcher_create_search_box.stop()
        self.patcher_create_edit_box.stop()
        self.patcher_create_action_information_box.stop()
        self.patcher_create_close_button.stop()
        self.ui_panel = None

    def test_init(self):
        self.assertEqual(self.ui_panel.window, self.mock_window)
        self.assertEqual(self.ui_panel.manager, self.mock_manager)
        self.assertEqual(self.ui_panel.width, 1000)
        self.assertEqual(self.ui_panel.height, 800)
        self.assertEqual(self.ui_panel.digraph, self.mock_digraph)
        self.assertEqual(self.ui_panel.base_panel, self.mock_create_base_panel.return_value)
        self.assertEqual(self.ui_panel.infos, self.mock_create_information_box.return_value)
        self.assertEqual(self.ui_panel.search_box, self.mock_create_search_box.return_value)
        self.assertEqual(self.ui_panel.edit_box, self.mock_create_edit_box.return_value)
        self.assertEqual(self.ui_panel.action_information, self.mock_create_action_information_box.return_value)

        self.mock_create_base_panel.assert_called_once_with()
        self.mock_create_information_box.assert_called_once_with()
        self.mock_create_search_box.assert_called_once_with()
        self.mock_create_edit_box.assert_called_once_with()
        self.mock_create_action_information_box.assert_called_once_with()
        self.mock_create_close_button.assert_called_once_with()

    def test_create_switch_panel(self):
        self.patcher_create_switch_panel.stop()
        ret_val = self.ui_panel.create_switch_panel()
        self.assertEqual(self.mock_pgui_elements.UIPanel.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UIButton.call_count, 2)
        self.assertEqual(len(ret_val.keys()), 3)

    def test_create_edit_box(self):
        self.patcher_create_edit_box.stop()
        ret_val = self.ui_panel.create_edit_box()
        self.assertEqual(self.mock_pgui_elements.UIPanel.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UILabel.call_count, 7)
        self.assertEqual(self.mock_pgui_elements.UITextEntryLine.call_count, 21)
        self.assertEqual(self.mock_pgui_elements.UIButton.call_count, 3)
        self.assertEqual(len(ret_val.keys()), 5)

    def test_create_search_box(self):
        self.patcher_create_search_box.stop()
        ret_val = self.ui_panel.create_search_box()
        self.assertEqual(self.mock_pgui_elements.UIPanel.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UILabel.call_count, 4)
        self.assertEqual(self.mock_pgui_elements.UITextEntryLine.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UIDropDownMenu.call_count, 4)
        self.assertEqual(self.mock_pgui_elements.UIButton.call_count, 4)
        self.assertEqual(len(ret_val.keys()), 14)

    def test_create_close_button(self):
        self.patcher_create_close_button.stop()
        ret_val = self.ui_panel.create_close_button()
        self.assertEqual(self.mock_pgui_elements.UIButton.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UIPanel.call_count, 1)

    def test_handle_close_button_pressed_closed(self):
        self.ui_panel.closed = True
        self.ui_panel.handle_close_button_pressed()
        self.assertFalse(self.ui_panel.closed)
        self.assertEqual(self.mock_create_close_button.call_count, 2)
        self.assertEqual(self.ui_panel.base_panel.show.call_count, 1)

    def test_handle_close_button_pressed(self):
        self.ui_panel.closed = False
        self.ui_panel.handle_close_button_pressed()
        self.assertTrue(self.ui_panel.closed)
        self.assertEqual(self.mock_create_close_button.call_count, 2)
        self.assertEqual(self.ui_panel.base_panel.hide.call_count, 1)

    def test_get_all_node_info_id(self):
        self.ui_panel.search_mode = "id"
        mock_node_1 = MagicMock()
        mock_node_1.id = 1
        mock_node_1.name = "node_1"
        mock_node_2 = MagicMock()
        mock_node_2.id = 2
        mock_node_2.name = "node_2"
        mock_node_3 = MagicMock()
        mock_node_3.id = 3
        mock_node_3.name = "node_3"
        self.mock_digraph.nodes = [mock_node_1, mock_node_2, mock_node_3]
        ret_val = self.ui_panel.get_all_node_info()
        self.assertEqual(ret_val, [1, 2, 3])

    def test_get_all_node_info_name(self):
        self.ui_panel.search_mode = "name"
        mock_node_1 = MagicMock()
        mock_node_1.id = 1
        mock_node_1.name = "node_1"
        mock_node_2 = MagicMock()
        mock_node_2.id = 2
        mock_node_2.name = "node_2"
        mock_node_3 = MagicMock()
        mock_node_3.id = 3
        mock_node_3.name = "node_3"
        self.mock_digraph.nodes = [mock_node_1, mock_node_2, mock_node_3]
        ret_val = self.ui_panel.get_all_node_info()
        self.assertEqual(ret_val, ["node_1", "node_2", "node_3"])

    def test_create_drop_down_menu(self):
        mock_dropdown = self.mock_pgui_elements.UIDropDownMenu.return_value = MagicMock()
        ret_val = self.ui_panel.create_drop_down_menu(None, None, MagicMock(), MagicMock(), MagicMock(), False)
        self.assertEqual(self.mock_pgui_elements.UIDropDownMenu.call_count, 1)
        self.assertEqual(ret_val, mock_dropdown)

    def test_filter_nodes_by_search(self):
        mock_node_1 = MagicMock()
        mock_node_1.id = "1"
        mock_node_1.name = "node_1"
        mock_node_2 = MagicMock()
        mock_node_2.id = "12"
        mock_node_2.name = "node_2"
        mock_node_3 = MagicMock()
        mock_node_3.id = "3"
        mock_node_3.name = "node_3"
        self.mock_digraph.nodes = [mock_node_1, mock_node_2, mock_node_3]
        self.ui_panel.search_box = MagicMock()
        self.ui_panel.search_box.get_text.return_value = "node_1"
        with patch.object(self.ui_panel, "create_drop_down_menu") as mock_create_drop_down_menu:
            (filtered_info, mode) = self.ui_panel.filter_nodes_by_search("1")
            mock_create_drop_down_menu.assert_called_once()
        self.assertEqual(filtered_info, ["1", "12"])

    def test_create_information_box(self):
        self.patcher_create_information_box.stop()
        ret_val = self.ui_panel.create_information_box()
        self.assertEqual(self.mock_pgui_elements.UIPanel.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UILabel.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UITextBox.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UIButton.call_count, 1)
        self.assertEqual(len(ret_val.keys()), 4)

    def test_recreate_show_popup_button(self):
        self.ui_panel.show_popup_button = MagicMock()
        self.ui_panel.recreate_show_popup_button()
        self.assertEqual(self.mock_pgui_elements.UIButton.call_count, 1)

    def test_create_action_information_box(self):
        self.patcher_create_action_information_box.stop()
        ret_val = self.ui_panel.create_action_information_box()
        self.assertEqual(self.mock_pgui_elements.UIPanel.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UILabel.call_count, 1)
        self.assertEqual(len(ret_val.keys()), 2)

    def test_handle_light_mode_pressed(self):
        with patch.object(self.ui_panel, "set_action_label") as mock_set_action_label:
            with patch.object(self.ui_panel, "change_color_text_entry_texts") as mock_change_color_text_entry_texts:
                ret_val = self.ui_panel.handle_light_mode_pressed()
                mock_set_action_label.assert_called_once()
                mock_change_color_text_entry_texts.assert_called_once()
        self.assertEqual(len(ret_val.keys()), 7)

    def test_handle_dark_mode_pressed(self):
        with patch.object(self.ui_panel, "set_action_label") as mock_set_action_label:
            with patch.object(self.ui_panel, "change_color_text_entry_texts") as mock_change_color_text_entry_texts:
                ret_val = self.ui_panel.handle_dark_mode_pressed()
                mock_set_action_label.assert_called_once()
                mock_change_color_text_entry_texts.assert_called_once()
        self.assertEqual(len(ret_val.keys()), 7)

    def test_handle_personal_mode_pressed(self):
        with patch.object(self.ui_panel, "set_action_label") as mock_set_action_label:
            ret_val = self.ui_panel.handle_personal_mode_pressed()
            mock_set_action_label.assert_called_once()
        self.assertEqual(len(ret_val.keys()), 7)

    def test_handle_search_bar_changed(self):
        with patch.object(self.ui_panel, "filter_nodes_by_search") as mock_filter_nodes_by_search:
            self.ui_panel.handle_search_bar_changed()
            mock_filter_nodes_by_search.assert_called_once()

    def handle_focus_button_pressed(self):
        with patch.object(self.ui_panel, "set_action_label") as mock_set_action_label:
            with patch.object(self.ui_panel, "update_information_box") as mock_update_information_box:
                self.ui_panel.handle_focus_button_pressed()
                mock_set_action_label.assert_called_once()
                mock_update_information_box.assert_called_once()

    def test_handle_search_by_id_button_pressed(self):
        self.ui_panel.search_mode = "name"
        with patch.object(self.ui_panel, "create_drop_down_menu") as mock_create_drop_down_menu:
            with patch.object(self.ui_panel, "get_all_node_info") as mock_get_all_node_info:
                self.ui_panel.handle_search_by_id_button_pressed()
                mock_create_drop_down_menu.assert_called_once()
                mock_get_all_node_info.assert_called_once()
        self.assertEqual(self.ui_panel.search_mode, "id")

    def test_handle_search_by_name_button_pressed(self):
        self.ui_panel.search_mode = "id"
        with patch.object(self.ui_panel, "create_drop_down_menu") as mock_create_drop_down_menu:
            with patch.object(self.ui_panel, "get_all_node_info") as mock_get_all_node_info:
                self.ui_panel.handle_search_by_name_button_pressed()
                mock_create_drop_down_menu.assert_called_once()
                mock_get_all_node_info.assert_called_once()
        self.assertEqual(self.ui_panel.search_mode, "name")

    def test_handle_switch_search_pressed(self):
        self.ui_panel.selected_mode = "edit"
        self.ui_panel.handle_switch_search_pressed()
        self.assertEqual(self.ui_panel.selected_mode, "search")

    def test_handle_switch_edit_pressed(self):
        self.ui_panel.selected_mode = "search"
        self.ui_panel.handle_switch_edit_pressed()
        self.assertEqual(self.ui_panel.selected_mode, "edit")

    def test_handle_popup_button_pressed(self):
        self.ui_panel.selected_node = MagicMock()
        self.ui_panel.handle_popup_button_pressed()
        self.assertEqual(self.mock_pgui_elements.UIWindow.call_count, 1)
        self.assertEqual(self.mock_pgui_elements.UIPanel.call_count, 1)

    def test_update_information_box(self):
        with patch.object(self.ui_panel, "recreate_show_popup_button") as mock_recreate_show_popup_button:
            self.ui_panel.update_information_box(MagicMock())
            mock_recreate_show_popup_button.assert_called_once()

    def test_create_base_panel(self):
        self.patcher_create_base_panel.stop()
        mock_panel =self.mock_pgui_elements.UIPanel.return_value = MagicMock()
        ret_val = self.ui_panel.create_base_panel()
        self.assertEqual(self.mock_pgui_elements.UIPanel.call_count, 1)
        self.assertEqual(ret_val, mock_panel)

    def test_set_action_label(self):
        mock_action_label = MagicMock()
        self.ui_panel.action_information = {'action_label': mock_action_label}
        self.ui_panel.set_action_label('other')
        mock_action_label.set_text.assert_called_once_with('other')

    def test_get_focused_node(self):
        mock_node = MagicMock()
        self.ui_panel.selected_node = mock_node
        focused_node = self.ui_panel.get_focused_node()
        self.assertEqual(focused_node, mock_node)

    def test_get_focused_depth(self):
        self.ui_panel.search_box['depth_choose'].selected_option = ['1']
        focused_depth = self.ui_panel.get_focused_depth()
        self.assertEqual(focused_depth, 1)

    def test_get_horizontal_scatter(self):
        self.ui_panel.search_box['horizontal_scatter_choose'].selected_option = ['1']
        horizontal_scatter = self.ui_panel.get_horizontal_scatter()
        self.assertEqual(horizontal_scatter, 1)

    def test_get_vertical_scatter(self):
        self.ui_panel.search_box['vertical_scatter_choose'].selected_option = ['1']
        vertical_scatter = self.ui_panel.get_vertical_scatter()
        self.assertEqual(vertical_scatter, 1)

    def test_is_name_specified(self):
        self.ui_panel.optional_pairings = {'node_name': 'None'}
        is_name_specified = self.ui_panel.is_name_specified()
        self.assertFalse(is_name_specified)

    def test_sub_id_value_names_specified(self):
        self.ui_panel.optional_pairings = {'sub_id_value_name': 'None'}
        is_sub_id_value_names_specified = self.ui_panel.sub_id_value_names_specified()
        self.assertFalse(is_sub_id_value_names_specified)

    def test_resize(self):
        self.ui_panel.close_button = MagicMock()
        self.ui_panel.resize(500, 600, self.mock_window, self.mock_manager)
        self.assertEqual(self.ui_panel.window, self.mock_window)
        self.assertEqual(self.ui_panel.manager, self.mock_manager)
        self.assertEqual(self.ui_panel.width, 500)
        self.assertEqual(self.ui_panel.height, 600)

    def test_process_events(self):
        event = MagicMock()
        self.ui_panel.process_events(event)

    def test_draw_ui(self):
        self.ui_panel.draw_ui()
        self.mock_manager.draw_ui.assert_called_once_with(self.mock_window)

    def test_get_manager(self):
        manager = self.ui_panel.get_manager()
        self.assertEqual(manager, self.mock_manager)

    def test_update(self):
        time_delta = 0.1
        self.ui_panel.update(time_delta)
        self.mock_manager.update.assert_called_once_with(time_delta)


if __name__ == '__main__':
    unittest.main()