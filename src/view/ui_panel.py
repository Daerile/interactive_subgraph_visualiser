import pygame as pg
import pygame_gui as pgui


class UIPanel:
    def __init__(self, window, manager, width, height, digraph, header_height):
        self.results_panel = None
        self.window = window
        self.width = width
        self.height = height
        self.manager = manager
        self.digraph = digraph
        self.header_height = header_height
        self.selected_node = None
        self.base_panel = self.create_base_panel()
        self.infos = self.create_information_box()
        self.search_box = self.create_search_box()
        self.popup = None

    def create_search_box(self):
        # Panel to contain the search elements
        search_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 0, self.width, 3 * self.height / 4),
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

        focus_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 90, self.width - 20, 30),
            text='Focus on Node',
            manager=self.manager,
            container=search_panel
        )
        return [search_panel, search_label, search_text, dropdown, focus_button]

    def get_all_node_ids(self):
        return [node.id for node in self.digraph.nodes]

    def create_drop_down_menu(self, options_list, starting_option, relative_rect, manager, container, update):
        if update:
            self.search_box[3].kill()
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
            self.search_box[3] = self.create_drop_down_menu(
                options_list=filtered_ids,
                starting_option=filtered_ids[0] if filtered_ids else 'None',
                relative_rect=pg.Rect(10, 50, self.width - 20, 30),
                manager=self.manager,
                container=self.search_box[0],
                update=True
            )
        else:
            self.search_box[3] = self.create_drop_down_menu(
                options_list=all_node_ids,
                starting_option=all_node_ids[0] if all_node_ids else 'None',
                relative_rect=pg.Rect(10, 50, self.width - 20, 30),
                manager=self.manager,
                container=self.search_box[0],
                update=True
            )

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

    def handle_search_bar_changed(self):
        self.filter_nodes_by_search(self.search_box[2].get_text())

    def handle_focus_button_pressed(self):
        selected_id = self.search_box[3].selected_option[0]
        if selected_id == 'No results found':
            return
        for node in self.digraph.nodes():
            if node.id == selected_id:
                self.update_information_box(node)
                break

    def handle_popup_button_pressed(self):
        # Create a popup window with appropriate dimensions
        self.popup = pgui.elements.UIWindow(
            rect=pg.Rect(100, 100, 400, 400),  # Size of the window
            manager=self.manager,
            window_display_title='Node Information',
            element_id='popup_window'
        )

        # Adjusting the scrolling container to fit the window's inner dimensions more accurately
        scrolling_container = pgui.elements.UIScrollingContainer(
            relative_rect=pg.Rect(10, 10, 380, 380),  # Slightly reduced size for padding
            manager=self.manager,
            container=self.popup
        )

        y_offset = 0

        if self.selected_node is None:
            text = '<p>No node selected!</p>'
            popup_text = pgui.elements.UITextBox(
                relative_rect=pg.Rect(0, y_offset, 360, 30),  # Adjust width to fit within scrolling container
                html_text=text,
                manager=self.manager,
                container=scrolling_container
            )
            y_offset += 35
        else:
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

        # Set the dimensions of the scrollable area based on content height
        scrolling_container.set_scrollable_area_dimensions((360, y_offset))

        self.popup.set_blocking(True)

    def update_information_box(self, node):
        self.selected_node = node
        self.infos[1].set_text(f'ID: {node.get_id()}')

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

    def killall(self):
        for element in self.infos:
            element.disable()
            element.kill()
        for element in self.search_box:
            element.disable()
            element.kill()
        self.base_panel.kill()
        self.infos = []
        self.search_box = []
        self.base_panel = None

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
