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
        # Adjust the information box to be at the bottom half of its container
        information_box = pgui.elements.UIPanel(
            relative_rect=pg.Rect(0, 3 * self.height / 4, self.width, 3 * self.height / 4),
            # Start at half height, take up half height
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

        # Correctly size and place the ID label
        id_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 10, self.width - 20, 30),  # Width minus padding, appropriate height
            text='ID: No node selected',
            manager=self.manager,
            container=information_box
        )

        # Correctly size and place the sub-ID label
        subid_label = pgui.elements.UILabel(
            relative_rect=pg.Rect(10, 50, self.width - 20, 30),  # Adjusted position below the ID label
            text='Sub ID: No node selected',
            manager=self.manager,
            container=information_box
        )

        # Adjust the dropdown to fit below the sub-ID label
        show_popup_button = pgui.elements.UIButton(
            relative_rect=pg.Rect(10, 90, self.width - 20, 40),
            text='Show Other Info',
            manager=self.manager,
            container=information_box
        )

        return information_box, id_label, subid_label, show_popup_button

    def handle_popup_button_pressed(self):
        popup = pgui.elements.UIWindow(
            rect=pg.Rect(100, 100, 400, 400),
            manager=self.manager,
            window_display_title='Other Information',
            element_id='popup_window'
        )

        text = ''
        if self.selected_node is None:
            text = 'No node selected!'
        else:
            other_attributes = self.selected_node.get_other_attributes()
            for key, value in other_attributes.items():
                text += f'{key}: {value}\n'

        popup_text = pgui.elements.UITextBox(
            relative_rect=pg.Rect(0, 0, 400, 400),
            html_text='<p>' + text + '</p>',
            manager=self.manager,
            container=popup
        )

        popup.set_blocking(True)

    def update_information_box(self, node):
        self.selected_node = node
        self.infos[1].set_text(f'ID: {node.get_id()}')
        self.infos[2].set_text(f'Sub ID: {node.get_sub_id()}')


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
