import pygame as pg
import pygame_gui as pgui


class UIPanel:
    def __init__(self, window, manager, width, height, digraph, focused_depth, header_height):
        self.results_panel = None
        self.window = window
        self.width = width
        self.height = height
        self.manager = manager
        self.digraph = digraph
        self.focused_depth = focused_depth
        self.header_height = header_height
        self.selected_node = None
        self.selected_edge = None
        self.selected_mode = 'search'
        self.base_panel = self.create_base_panel()
        self.switch_panel = self.create_switch_panel()
        self.infos = self.create_information_box()
        self.search_box = self.create_search_box()
        self.edit_box = self.create_edit_box()
        self.action_information = self.create_action_information_box()
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
            text='Edit',
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

        edit_panel.hide()
        items_map = {
            'edit_panel': edit_panel,
            'dark_mode': dark_mode_button,
            'light_mode': light_mode_button
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

        # Label for the search box
        search_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 10, 100, 30),
            text="Search:",
            manager=self.manager,
            container=search_panel
        )

        # Text entry for searching nodes
        search_text = pgui.elements.UITextEntryLine(
            relative_rect=pg.Rect(120, 10, self.width - 130, 30),
            manager=self.manager,
            container=search_panel
        )

        # Dropdown menu initialized with all node IDs
        all_ids = self.get_all_node_ids()

        dropdown = self.create_drop_down_menu(
            options_list=all_ids,
            starting_option=all_ids[0] if all_ids else 'None',
            relative_rect=pg.Rect(10, 50, self.width - 20, 30),
            manager=self.manager,
            container=search_panel,
            update=False
        )

        depth_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 90, 100, 30),
            text="Depth:",
            manager=self.manager,
            container=search_panel
        )

        depth_choose = pgui.elements.UIDropDownMenu(
            options_list=[str(i) for i in range(1, 5)],
            starting_option=str(self.focused_depth),
            relative_rect=pg.Rect(120, 90, self.width - 130, 30),
            manager=self.manager,
            container=search_panel
        )

        focus_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 130, self.width - 20, 30),
            text='Focus on Node',
            manager=self.manager,
            container=search_panel
        )

        return_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 170, self.width - 20, 30),
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
            'return_button': return_button
        }
        return return_map

    def get_all_node_ids(self):
        return [node.id for node in self.digraph.nodes]

    def create_drop_down_menu(self, options_list, starting_option, relative_rect, manager, container, update):
        if update:
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
        all_node_ids = self.get_all_node_ids()
        if query:
            filtered_ids = [node_id for node_id in all_node_ids if query.lower() in node_id.lower()]
            if not filtered_ids:
                filtered_ids = ['No results found']
            self.search_box['dropdown'] = self.create_drop_down_menu(
                options_list=filtered_ids,
                starting_option=filtered_ids[0] if filtered_ids else 'None',
                relative_rect=pg.Rect(10, 50, self.width - 20, 30),
                manager=self.manager,
                container=self.search_box['search_panel'],
                update=True
            )
            if not filtered_ids:
                return None
            return filtered_ids
        else:
            self.search_box['dropdown'] = self.create_drop_down_menu(
                options_list=all_node_ids,
                starting_option=all_node_ids[0] if all_node_ids else 'None',
                relative_rect=pg.Rect(10, 50, self.width - 20, 30),
                manager=self.manager,
                container=self.search_box['search_panel'],
                update=True
            )
            return None

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

        show_popup_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 50, self.width - 20, 40),
            text='Show Other Info',
            manager=self.manager,
            container=information_box
        )

        return information_box, id_label, show_popup_button

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
        colors = {
            'background': (240,240,240),
            'text': pg.Color('white'),
            'node': (0, 156, 235),
            'edge': (136, 136, 136),
            'selected_node': (220, 247, 99),
            'searched_node': (255, 155, 113),
            'selected_edge': (0, 0, 0)
        }

        return colors

    def handle_dark_mode_pressed(self):
        self.set_action_label('Theme set to dark mode')
        colors = {
            'background': (1, 28, 39),
            'text': pg.Color('black'),
            'node': (131, 119, 209),
            'edge': (136,136,136),
            'selected_node': (252, 163, 17),
            'searched_node': (228, 187, 151),
            'selected_edge': (255, 255, 255)
        }

        return colors

    def handle_search_bar_changed(self):
        return self.filter_nodes_by_search(self.search_box['search_text'].get_text())

    def handle_focus_button_pressed(self):
        selected_id = self.search_box['dropdown'].selected_option[0]
        if selected_id == 'No results found' or selected_id == 'None':
            self.set_action_label('Cannot set focus to no node in dropdown!')
            return
        for node in self.digraph.nodes():
            if node.id == selected_id:
                self.set_action_label(f'Focus set to {node.id}')
                self.update_information_box(node)
                break

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
            rect=pg.Rect(100, 100, 400, 400),  # Size of the window
            manager=self.manager,
            window_display_title='Additional Information',
            element_id='popup_window'
        )

        # Adjusting the scrolling container to fit the window's inner dimensions more accurately
        scrolling_container = pgui.elements.UIScrollingContainer(
            relative_rect=pg.Rect(10, 10, 380, 380),  # Slightly reduced size for padding
            manager=self.manager,
            container=self.popup
        )

        y_offset = 0

        if self.selected_node is None and self.selected_edge is None:
            text = '<p>No node selected!</p>'
            popup_text = pgui.elements.UITextBox(
                relative_rect=pg.Rect(0, y_offset, 360, 30),  # Adjust width to fit within scrolling container
                html_text=text,
                manager=self.manager,
                container=scrolling_container
            )
            y_offset += 35
        elif self.selected_node is not None:
            attributes = self.selected_node.get_attributes()
            if not attributes:
                text = '<p>No attributes!</p>'
                popup_text = pgui.elements.UITextBox(
                    relative_rect=pg.Rect(0, y_offset, 360, 30),
                    html_text=text,
                    manager=self.manager,
                    container=scrolling_container
                )
                y_offset += 35
            else:
                for key, value in attributes.items():
                    if key == 'connections':
                        if not value:
                            text = '<p>No connections!</p>'
                            popup_text = pgui.elements.UITextBox(
                                relative_rect=pg.Rect(0, y_offset, 360, 30),
                                html_text=text,
                                manager=self.manager,
                                container=scrolling_container
                            )
                            y_offset += 35
                            break
                        for subkey, sublist in value.items():
                            label = pgui.elements.UILabel(
                                relative_rect=pg.Rect(0, y_offset, 360, 30),
                                text=f'{subkey}:',
                                manager=self.manager,
                                container=scrolling_container
                            )
                            y_offset += 35
                            dropdown = pgui.elements.UIDropDownMenu(
                                options_list=sublist,
                                starting_option=sublist[0] if sublist else 'None',
                                relative_rect=pg.Rect(0, y_offset, 360, 30),
                                manager=self.manager,
                                container=scrolling_container
                            )
                            y_offset += 35
                    else:
                        text = f'<p><b>{key}:</b> {value}</p>'
                        popup_text = pgui.elements.UITextBox(
                            relative_rect=pg.Rect(0, y_offset, 360, 30),
                            html_text=text,
                            manager=self.manager,
                            container=scrolling_container
                        )
                        y_offset += 35
        else:
            text = f'<p>Edge: {self.selected_edge[0].id} - {self.selected_edge[1].id}</p>'
            popup_text = pgui.elements.UITextBox(
                relative_rect=pg.Rect(0, y_offset, 360, 30),
                html_text=text,
                manager=self.manager,
                container=scrolling_container
            )
            y_offset += 35

        # Set the dimensions of the scrollable area based on content height
        scrolling_container.set_scrollable_area_dimensions((360, y_offset))

        self.popup.set_blocking(True)

    def update_information_box(self, selected_item, edge=False):
        if edge:
            self.infos[1].set_text(f'Edge: {selected_item[0].id} - {selected_item[1].id}')
            self.selected_node = None
            self.selected_edge = selected_item
        else:
            self.selected_node = selected_item
            self.infos[1].set_text(f'ID: {selected_item.get_id()}')
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
        for element in self.infos:
            element.disable()
            element.kill()
        for element in self.search_box.values():
            element.disable()
            element.kill()
        self.base_panel.kill()
        self.infos = []
        self.search_box = {}
        self.base_panel = None

    def get_focused_node(self):
        return self.selected_node

    def get_focused_depth(self):
        return int(self.search_box['depth_choose'].selected_option[0])

    def process_events(self, event):
        # this works but I dont know why
        # self.manager.process_events(event)
        e = []

    def draw_ui(self):
        self.manager.draw_ui(self.window)

    def get_manager(self):
        return self.manager

    def update(self, time_delta):
        self.manager.update(time_delta)
