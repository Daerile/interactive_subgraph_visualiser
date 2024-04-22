import pygame as pg
import pygame_gui as pgui


class UIPanel:
    def __init__(self, window, manager, width, height):
        self.window = window
        self.width = width
        self.height = height
        self.manager = manager
        self.selected_node = None
        self.base_panel = self.create_base_panel()
        self.create_search_box()
        self.infos = self.create_information_box()


    def create_search_box(self):
        search_box = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 0, self.width, 3 * self.height / 4),
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

        search_text = pgui.elements.UITextEntryLine(
            relative_rect=pg.Rect(10, 10, self.width - 20, 30),
            manager=self.manager,
            container=search_box
        )

        # TODO finish this

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

    def handle_popup_button_pressed(self):
        # Create a popup window with appropriate dimensions
        popup = pgui.elements.UIWindow(
            rect=pg.Rect(100, 100, 400, 400),  # Size of the window
            manager=self.manager,
            window_display_title='Node Information',
            element_id='popup_window'
        )

        # Adjusting the scrolling container to fit the window's inner dimensions more accurately
        scrolling_container = pgui.elements.UIScrollingContainer(
            relative_rect=pg.Rect(10, 10, 380, 380),  # Slightly reduced size for padding
            manager=self.manager,
            container=popup
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

        popup.set_blocking(True)

    def update_information_box(self, node):
        self.selected_node = node
        self.infos[1].set_text(f'ID: {node.get_id()}')

    def create_base_panel(self):
        base_panel = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 0, self.width, self.height),
            starting_height=0,
            manager=self.manager,
            anchors={'left': 'left',
                     'right': 'right',
                     'top': 'top',
                     'bottom': 'bottom'}
        )
        return base_panel

    def process_events(self, event):
        self.manager.process_events(event)

    def update(self, time_delta):
        self.manager.update(time_delta)

    def draw_ui(self):
        self.manager.draw_ui(self.window)

    def get_manager(self):
        return self.manager
