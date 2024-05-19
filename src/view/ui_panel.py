import pygame as pg
import pygame_gui as pgui


class UIPanel:
    def __init__(self, window, manager, width, height, digraph, focused_depth, vertical_scatter, horizontal_scatter,
                 header_height, colors=None, optional_pairings=None):
        if colors is not None:
            self.colors = colors
        else:
            self.colors = {
                'background': (240, 240, 240),
                'text': pg.Color('black'),
                'node': (0, 156, 235),
                'edge': (136, 136, 136),
                'selected_node': (220, 247, 99),
                'searched_node': (255, 155, 113),
                'selected_edge': (0, 0, 0)
            }
        self.search_mode = 'id'
        self.optional_pairings = optional_pairings
        self.results_panel = None
        self.window = window
        self.width = width
        self.height = height
        self.manager = manager
        self.digraph = digraph
        self.focused_depth = focused_depth
        self.vertical_scatter = vertical_scatter
        self.horizontal_scatter = horizontal_scatter
        self.header_height = header_height
        self.selected_node = None
        self.selected_edge = None
        self.selected_mode = 'search'
        self.base_panel = self.create_base_panel()
        self.closed = False
        self.switch_panel = self.create_switch_panel()
        self.infos = self.create_information_box()
        self.search_box = self.create_search_box()
        self.edit_box = self.create_edit_box()
        self.action_information = self.create_action_information_box()
        self.close_button = self.create_close_button()
        self.popup = None

    def create_switch_panel(self):
        switch_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 0, self.width, 50),
            manager=self.manager,
            container=self.base_panel
        )

        button_width = (self.width - 30) // 2

        # Define the Search button
        switch_search = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 10, button_width, 30),
            text='Search',
            manager=self.manager,
            container=switch_panel
        )

        switch_edit = pgui.elements.UIButton(
            relative_rect=pg.Rect(20 + button_width, 10, button_width, 30),
            text='Edit colors',
            manager=self.manager,
            container=switch_panel
        )

        item_map = {
            'panel': switch_panel,
            'search': switch_search,
            'edit': switch_edit
        }

        return item_map

    def create_edit_box(self):
        starting_height = self.switch_panel['panel'].get_relative_rect().height
        edit_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, starting_height, self.width, self.height / 2 + 50),
            starting_height=starting_height,
            manager=self.manager,
            container=self.base_panel
        )

        button_width = (self.width - 30) // 2  # Divides the available width into two, leaving some space between buttons

        dark_mode_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 10, button_width, 30),  # Positioned on the left
            text='Toggle Dark Mode',
            manager=self.manager,
            container=edit_panel
        )

        light_mode_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(20 + button_width, 10, button_width, 30),  # Positioned on the right
            text='Toggle Light Mode',
            manager=self.manager,
            container=edit_panel
        )

        needed_colors = ['background', 'text', 'node', 'edge', 'selected_node', 'searched_node', 'selected_edge']
        color_dict = {}
        for color in needed_colors:
            color_label = pgui.elements.UILabel(
                relative_rect=pg.Rect(10, 50 + 40 * needed_colors.index(color), 100, 30),
                text=f'{color.capitalize()}:',
                manager=self.manager,
                container=edit_panel
            )
            color_text_red = pgui.elements.UITextEntryLine(
                relative_rect=pg.Rect(120, 50 + 40 * needed_colors.index(color), 50, 30),
                manager=self.manager,
                initial_text=str(self.colors[color][0]),
                container=edit_panel
            )
            color_text_green = pgui.elements.UITextEntryLine(
                relative_rect=pg.Rect(180, 50 + 40 * needed_colors.index(color), 50, 30),
                manager=self.manager,
                initial_text=str(self.colors[color][1]),
                container=edit_panel
            )
            color_text_blue = pgui.elements.UITextEntryLine(
                relative_rect=pg.Rect(240, 50 + 40 * needed_colors.index(color), 50, 30),
                manager=self.manager,
                initial_text=str(self.colors[color][2]),
                container=edit_panel
            )

            color_dict[color] = {
                'red': color_text_red,
                'green': color_text_green,
                'blue': color_text_blue
            }

        personal_colors_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 50 + 40 * len(needed_colors), self.width - 20, 30),
            text='Set Colors',
            manager=self.manager,
            container=edit_panel
        )

        edit_panel.hide()
        items_map = {
            'edit_panel': edit_panel,
            'dark_mode': dark_mode_button,
            'light_mode': light_mode_button,
            'colors': color_dict,
            'personal_mode': personal_colors_button
        }

        return items_map

    def create_search_box(self):
        starting_height = self.switch_panel['panel'].get_relative_rect().height
        # Panel to contain the search elements
        search_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, starting_height, self.width, self.height / 2 + 50),
            starting_height=starting_height,
            manager=self.manager,
            container=self.base_panel
        )

        button_width = (self.width - 30) // 2

        search_by_id_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 10, button_width, 30),
            text='Search by ID',
            manager=self.manager,
            container=search_panel
        )

        search_by_name_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(20 + button_width, 10, button_width, 30),
            text='Search by Name',
            manager=self.manager,
            container=search_panel
        )

        search_by_id_button.disable()
        if self.optional_pairings is None or self.optional_pairings['node_name'] == 'None':
            search_by_name_button.disable()

        # Label for the search box
        search_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 50, 100, 30),
            text="Search:",
            manager=self.manager,
            container=search_panel
        )

        # Text entry for searching nodes
        search_text = pgui.elements.UITextEntryLine(
            relative_rect=pg.Rect(120, 50, self.width - 130, 30),
            manager=self.manager,
            container=search_panel
        )

        # Dropdown menu initialized with all node IDs
        all_infos = self.get_all_node_info()

        dropdown = self.create_drop_down_menu(
            options_list=all_infos,
            starting_option=all_infos[0] if all_infos else 'None',
            relative_rect=pg.Rect(10, 90, self.width - 20, 30),
            manager=self.manager,
            container=search_panel,
            update=False
        )

        depth_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 130, 200, 30),
            text="Depth:",
            manager=self.manager,
            container=search_panel
        )

        depth_choose = pgui.elements.UIDropDownMenu(
            options_list=[str(i) for i in range(1, 6)],
            starting_option=str(self.focused_depth),
            relative_rect=pg.Rect(220, 130, self.width - 230, 30),
            manager=self.manager,
            container=search_panel
        )

        horizontal_scatter_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 170, 200, 30),
            text="Horizontal Scatter:",
            manager=self.manager,
            container=search_panel
        )

        horizontal_scatter_choose = pgui.elements.UIDropDownMenu(
            options_list=[str(i) for i in range(1, 6)],
            starting_option=str(self.horizontal_scatter),
            relative_rect=pg.Rect(220, 170, self.width - 230, 30),
            manager=self.manager,
            container=search_panel
        )

        vertical_scatter_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 210, 200, 30),
            text="Vertical Scatter:",
            manager=self.manager,
            container=search_panel
        )

        vertical_scatter_choose = pgui.elements.UIDropDownMenu(
            options_list=[str(i) for i in range(1, 6)],
            starting_option=str(self.vertical_scatter),
            relative_rect=pg.Rect(220, 210, self.width - 230, 30),
            manager=self.manager,
            container=search_panel
        )

        focus_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 250, self.width - 20, 30),
            text='Focus on Node',
            manager=self.manager,
            container=search_panel
        )

        return_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 290, self.width - 20, 30),
            text='Return to Full Graph',
            manager=self.manager,
            container=search_panel
        )

        return_map = {
            'search_panel': search_panel,
            'search_label': search_label,
            'search_text': search_text,
            'dropdown': dropdown,
            'focus_button': focus_button,
            'depth_label': depth_label,
            'depth_choose': depth_choose,
            'horizontal_scatter_label': horizontal_scatter_label,
            'horizontal_scatter_choose': horizontal_scatter_choose,
            'vertical_scatter_label': vertical_scatter_label,
            'vertical_scatter_choose': vertical_scatter_choose,
            'return_button': return_button,
            'search_by_id_button': search_by_id_button,
            'search_by_name_button': search_by_name_button
        }
        return return_map

    def create_close_button(self):
        # Make sure this panel is very close to the top of the z-order by recreating it last
        close_button_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, self.height - 40, 30, 40),
            starting_height=self.height - 40,  # Ensure it's towards the bottom of the window
            manager=self.manager
        )
        close_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(0, 5, 30, 30),  # Small adjustment for vertical centering in the panel
            text='X',
            manager=self.manager,
            container=close_button_panel
        )

        return close_button

    def handle_close_button_pressed(self):
        if self.closed:
            self.closed = False
            self.close_button.set_text('X')
            self.base_panel.show()
            if self.selected_mode == 'search':
                self.edit_box['edit_panel'].hide()
            else:
                self.search_box['search_panel'].hide()
        else:
            self.closed = True
            self.close_button.set_text('O')
            self.base_panel.hide()

    def get_all_node_info(self):
        if self.search_mode == 'id':
            return [node.id for node in self.digraph.nodes]
        else:
            ret = [node.name for node in self.digraph.nodes if isinstance(node.name, str)]
            return ret

    def create_drop_down_menu(self, options_list, starting_option, relative_rect, manager, container, update):
        if update:
            self.search_box['dropdown'].hide()
            self.search_box['dropdown'].kill()
        dropdown = pgui.elements.UIDropDownMenu(
            options_list=options_list if options_list else ['None'],
            starting_option=starting_option if options_list else 'None',
            relative_rect=relative_rect,
            manager=manager,
            container=container
        )
        return dropdown

    def filter_nodes_by_search(self, query):
        all_node_info = self.get_all_node_info()
        if query:
            if self.search_mode == 'id':
                filtered_info = [node_id for node_id in all_node_info if query.lower() in node_id.lower()]
            else:
                filtered_info = [node_name for node_name in all_node_info if query.lower() in node_name.lower()]
            if not filtered_info:
                filtered_info = ['No results found']
            self.search_box['dropdown'] = self.create_drop_down_menu(
                options_list=filtered_info,
                starting_option=filtered_info[0] if filtered_info else 'None',
                relative_rect=pg.Rect(10, 90, self.width - 20, 30),
                manager=self.manager,
                container=self.search_box['search_panel'],
                update=True
            )
            if not filtered_info:
                return None, None
            return filtered_info, self.search_mode
        else:
            self.search_box['dropdown'].hide()
            self.search_box['dropdown'].kill()
            self.search_box['dropdown'] = self.create_drop_down_menu(
                options_list=all_node_info,
                starting_option=all_node_info[0] if all_node_info else 'None',
                relative_rect=pg.Rect(10, 90, self.width - 20, 30),
                manager=self.manager,
                container=self.search_box['search_panel'],
                update=True
            )
            return None, None

    def create_information_box(self):
        information_box = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 3 * self.height / 4, self.width, 3 * self.height / 4),
            starting_height=0,
            manager=self.manager,
            anchors={
                'left': 'left',
                'right': 'right',
                'top': 'top',
                'bottom': 'bottom'
            },
            container=self.base_panel
        )

        id_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 10, self.width - 20, 30),  # Width minus padding, appropriate height
            text='ID: No node selected',
            manager=self.manager,
            container=information_box
        )

        name_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 50, self.width - 20, 30),
            text=f'No node selected or no name specified',
            manager=self.manager,
            container=information_box
        )

        show_popup_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 90, self.width - 20, 40),
            text='Show Other Info',
            manager=self.manager,
            container=information_box
        )

        info_box = {
            'panel': information_box,
            'id_label': id_label,
            'show_popup_button': show_popup_button,
            'name_label': name_label
        }

        return info_box

    def create_action_information_box(self):
        # Determine the height position based on the previous element, e.g., search box
        starting_height = self.switch_panel['panel'].get_relative_rect().height + self.search_box[
            'search_panel'].get_relative_rect().height

        # Create a panel for action information messages
        action_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, starting_height - 5, self.width, 82),  # Adjust the height as needed
            manager=self.manager,
            container=self.base_panel
        )

        # Label for displaying messages
        action_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 10, self.width - 20, 30),
            text="No actions or errors",
            manager=self.manager,
            container=action_panel
        )

        return {'action_panel': action_panel, 'action_label': action_label}

    def handle_light_mode_pressed(self):
        self.set_action_label('Theme set to light mode')
        self.colors = {
            'background': (240, 240, 240),
            'text': pg.Color('white'),
            'node': (0, 156, 235),
            'edge': (136, 136, 136),
            'selected_node': (220, 247, 99),
            'searched_node': (255, 155, 113),
            'selected_edge': (0, 0, 0)
        }
        self.change_color_text_entry_texts()

        return self.colors

    def handle_dark_mode_pressed(self):
        self.set_action_label('Theme set to dark mode')
        self.colors = {
            'background': (1, 28, 39),
            'text': pg.Color('black'),
            'node': (131, 119, 209),
            'edge': (136, 136, 136),
            'selected_node': (252, 163, 17),
            'searched_node': (228, 187, 151),
            'selected_edge': (255, 255, 255)
        }
        self.change_color_text_entry_texts()

        return self.colors

    def handle_personal_mode_pressed(self):
        for color, text_entries in self.edit_box['colors'].items():
            red = int(text_entries['red'].get_text())
            green = int(text_entries['green'].get_text())
            blue = int(text_entries['blue'].get_text())
            self.colors[color] = (red, green, blue)
        self.set_action_label('Personal colors set!')
        return self.colors

    def change_color_text_entry_texts(self):
        for color, text_entries in self.edit_box['colors'].items():
            text_entries['red'].set_text(str(self.colors[color][0]))
            text_entries['green'].set_text(str(self.colors[color][1]))
            text_entries['blue'].set_text(str(self.colors[color][2]))

    def handle_search_bar_changed(self):
        return self.filter_nodes_by_search(self.search_box['search_text'].get_text())

    def handle_focus_button_pressed(self):
        selected_info = self.search_box['dropdown'].selected_option[0]
        if selected_info == 'No results found' or selected_info == 'None':
            self.set_action_label('Cannot set focus to no node in dropdown!')
            return
        if self.search_mode == 'id':
            for node in self.digraph.nodes():
                if node.id == selected_info:
                    self.set_action_label(f'Focus set to {node.id}')
                    self.update_information_box(node)
                    break
        else:
            for node in self.digraph.nodes():
                if node.name == selected_info:
                    self.set_action_label(f'Focus set to {node.name}')
                    self.update_information_box(node)
                    break

    def handle_search_by_id_button_pressed(self):
        self.search_mode = 'id'
        if not (self.optional_pairings is None or self.optional_pairings['node_name'] == 'None'):
            self.search_box['search_by_name_button'].enable()
        self.search_box['search_by_id_button'].disable()
        all_node_info = self.get_all_node_info()
        self.search_box['dropdown'].hide()
        self.search_box['dropdown'].kill()
        self.search_box['dropdown'] = self.create_drop_down_menu(
            options_list=all_node_info,
            starting_option=all_node_info[0] if all_node_info else 'None',
            relative_rect=pg.Rect(10, 90, self.width - 20, 30),
            manager=self.manager,
            container=self.search_box['search_panel'],
            update=True
        )

    def handle_search_by_name_button_pressed(self):
        self.search_mode = 'name'
        self.search_box['search_by_id_button'].enable()
        self.search_box['search_by_name_button'].disable()
        all_node_info = self.get_all_node_info()
        self.search_box['dropdown'].hide()
        self.search_box['dropdown'].kill()
        self.search_box['dropdown'] = self.create_drop_down_menu(
            options_list=all_node_info,
            starting_option=all_node_info[0] if all_node_info else 'None',
            relative_rect=pg.Rect(10, 90, self.width - 20, 30),
            manager=self.manager,
            container=self.search_box['search_panel'],
            update=True
        )

    def handle_switch_search_pressed(self):
        if self.selected_mode == 'search':
            self.set_action_label('Already in search mode!')
            return
        self.selected_mode = 'search'
        self.search_box['search_panel'].show()
        self.edit_box['edit_panel'].hide()

    def handle_switch_edit_pressed(self):
        if self.selected_mode == 'edit':
            self.set_action_label('Already in edit mode!')
            return
        self.selected_mode = 'edit'
        self.search_box['search_panel'].hide()
        self.edit_box['edit_panel'].show()

    def handle_popup_button_pressed(self):
        # Create a popup window with appropriate dimensions
        self.popup = pgui.elements.UIWindow(
            rect=pg.Rect(100, 100, 600, 600),  # Size of the window
            manager=self.manager,
            window_display_title='Additional Information',
            element_id='popup_window'
        )

        # Adjusting the scrolling container to fit the window's inner dimensions more accurately
        panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 0, 600, 600),  # Slightly reduced size for padding
            manager=self.manager,
            container=self.popup
        )

        y_offset = 0

        if self.selected_node is None and self.selected_edge is None:
            text = 'No node selected!'
            popup_text = pgui.elements.UILabel(
                relative_rect=pg.Rect(0, y_offset, 560, 30),  # Adjust width to fit within scrolling container
                text=text,
                manager=self.manager,
                container=panel
            )
            y_offset += 35
        elif self.selected_node is not None:
            attributes = self.selected_node.attributes
            if not attributes:
                text = 'No attributes!'
                popup_text = pgui.elements.UILabel(
                    relative_rect=pg.Rect(0, y_offset, 560, 30),
                    text=text,
                    manager=self.manager,
                    container=panel
                )
                y_offset += 35
            else:
                for key, value in attributes.items():
                    if key == 'connections':
                        if not value or value == 'None':
                            text = 'No connections!'
                            popup_text = pgui.elements.UILabel(
                                relative_rect=pg.Rect(20, y_offset, 560, 30),
                                text=text,
                                manager=self.manager,
                                container=panel
                            )
                            y_offset += 35
                            break
                        for subkey, sublist in value.items():
                            subkey_text = str(subkey)
                            if self.is_name_specified():
                                subkey_text = str(str(subkey) + ': ' + self.selected_node.names[str(subkey)])
                                for item in sublist:
                                    for node in self.digraph.nodes:
                                        if node.id == item:
                                            sublist[sublist.index(item)] = str(str(item) + ': ' + node.name)
                            label = pgui.elements.UILabel(
                                relative_rect=pg.Rect(20, y_offset, 560, 30),
                                text=f'{subkey_text}:',
                                manager=self.manager,
                                container=panel
                            )
                            y_offset += 35
                            dropdown = pgui.elements.UIDropDownMenu(
                                options_list=sublist if sublist else ['None'],
                                starting_option=sublist[0] if sublist else 'None',
                                relative_rect=pg.Rect(20, y_offset, 560, 30),
                                manager=self.manager,
                                container=panel
                            )

                            if self.sub_id_value_names_specified():
                                y_offset += 35
                                sub_id_name_label = pgui.elements.UILabel(
                                    relative_rect=pg.Rect(20, y_offset, 560, 30),
                                    text=f'Sub_id value: {self.selected_node.sub_id_value_names[str(subkey)]}',
                                    manager=self.manager,
                                    container=panel
                                )
                            y_offset += 35
                    else:
                        item_label = pgui.elements.UILabel(
                            relative_rect=pg.Rect(0, y_offset, 560, 30),
                            text=f'{key}: {value}',
                            manager=self.manager,
                            container=panel
                        )
                        y_offset += 35
        else:
            if self.is_name_specified():
                text = f'Edge: {self.selected_edge[0].id}: {self.selected_edge[0].name} - {self.selected_edge[1].id}: {self.selected_edge[1].name}'
            else:
                text = f'Edge: {self.selected_edge[0].id} - {self.selected_edge[1].id}'
            popup_text = pgui.elements.UILabel(
                relative_rect=pg.Rect(0, y_offset, 560, 30),
                text=text,
                manager=self.manager,
                container=panel
            )
            y_offset += 35

        self.popup.set_blocking(True)

    def update_information_box(self, selected_item, edge=False):
        if edge:
            self.infos['id_label'].set_text(f'Edge: {selected_item[0].id} - {selected_item[1].id}')
            if selected_item[0].name is None or selected_item[1].name is None:
                self.infos['name_label'].set_text('No name specified')
            self.infos['name_label'].set_text(f'{selected_item[0].name} - {selected_item[1].name}')
            self.selected_node = None
            self.selected_edge = selected_item
        else:
            self.selected_node = selected_item
            self.infos['id_label'].set_text(f'ID: {selected_item.id}')
            if selected_item.name is None:
                self.infos['name_label'].set_text('No name specified')
            self.infos['name_label'].set_text(f'Name: {selected_item.name}')
            self.selected_edge = None

    def create_base_panel(self):
        base_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, self.header_height - 5, self.width, self.height),
            starting_height=self.header_height,
            manager=self.manager,
            anchors={'left': 'left',
                     'right': 'right',
                     'top': 'top',
                     'bottom': 'bottom'}
        )
        return base_panel

    def set_action_label(self, text):
        self.action_information['action_label'].set_text(text)

    def killall(self):
        for element in self.infos.values():
            if element == 'No name specified':
                continue
            element.disable()
            element.kill()
        for element in self.search_box.values():
            element.disable()
            element.kill()
        self.close_button.disable()
        self.close_button.kill()
        self.close_button = None
        self.base_panel.kill()
        self.infos = {}
        self.search_box = {}
        self.base_panel = None

    def get_focused_node(self):
        return self.selected_node

    def get_focused_depth(self):
        return int(self.search_box['depth_choose'].selected_option[0])

    def get_horizontal_scatter(self):
        return int(self.search_box['horizontal_scatter_choose'].selected_option[0])

    def get_vertical_scatter(self):
        return int(self.search_box['vertical_scatter_choose'].selected_option[0])

    def is_name_specified(self):
        if self.optional_pairings is None or self.optional_pairings['node_name'] == 'None':
            return False
        return True

    def sub_id_value_names_specified(self):
        if self.optional_pairings is None or self.optional_pairings['sub_id_value_name'] == 'None':
            return False
        return True

    def process_events(self, event):
        e = []

    def draw_ui(self):
        self.manager.draw_ui(self.window)

    def get_manager(self):
        return self.manager

    def update(self, time_delta):
        self.manager.update(time_delta)
